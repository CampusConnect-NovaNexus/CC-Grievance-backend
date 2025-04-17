# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON
from sentence_transformers import SentenceTransformer
import pgvector
from pgvector.sqlalchemy import Vector
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
pgvector.register_vector(db.engine)

# Initialize sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# ================== Database Models ==================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='student')
    department = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Complaint(db.Model):
    __tablename__ = 'complaints'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    status = db.Column(db.String(20), default='pending')
    upvotes = db.Column(db.Integer, default=0)
    metadata = db.Column(JSON)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref='complaints')
    category = db.relationship('Category', backref='complaints')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(50))

class ComplaintEmbedding(db.Model):
    __tablename__ = 'complaint_embeddings'
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'))
    embedding = db.Column(Vector(384))  # Match model dimension
    text = db.Column(db.Text)

    complaint = db.relationship('Complaint', backref='embedding')

# ================== API Endpoints ==================
@app.route('/api/complaints', methods=['POST'])
def create_complaint():
    data = request.json
    user_id = data['user_id']
    complaint_text = data['description']
    
    # Generate embedding
    embedding = model.encode(complaint_text)
    
    # Find similar complaints
    similar_complaints = ComplaintEmbedding.query.order_by(
        ComplaintEmbedding.embedding.l2_distance(embedding)
    ).limit(5).all()
    
    # Prepare suggestions
    suggestions = [{
        'id': c.complaint_id,
        'title': c.complaint.title,
        'similarity': 1 - (distance / 2)  # Convert L2 distance to cosine similarity
    } for c in similar_complaints if c.complaint_id]
    
    return jsonify({'suggestions': suggestions})

@app.route('/api/complaints/finalize', methods=['POST'])
def finalize_complaint():
    data = request.json
    user_id = data['user_id']
    complaint_data = data['complaint']
    
    if data.get('existing_complaint_id'):
        # Upvote existing complaint
        complaint = Complaint.query.get(data['existing_complaint_id'])
        complaint.upvotes += 1
        db.session.commit()
        return jsonify({'message': 'Complaint upvoted'})
    else:
        # Create new complaint
        new_complaint = Complaint(
            user_id=user_id,
            title=complaint_data['title'],
            description=complaint_data['description'],
            category_id=complaint_data.get('category_id'),
            metadata={
                'device': request.user_agent.string,
                'ip': request.remote_addr
            }
        )
        db.session.add(new_complaint)
        db.session.commit()
        
        # Store embedding
        embedding = model.encode(complaint_data['description'])
        db.session.add(ComplaintEmbedding(
            complaint_id=new_complaint.id,
            embedding=embedding,
            text=complaint_data['description']
        ))
        db.session.commit()
        
        return jsonify({'message': 'Complaint created', 'id': new_complaint.id})

if __name__ == '__main__':
    app.run()