from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import uuid
# Create db instance without app
db = SQLAlchemy()

# Complaint Model
class Complaint(db.Model):
    __tablename__ = 'complaint'

    user_id = db.Column(db.String, nullable=False)
    c_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4())) 
    complaint_message = db.Column(db.String(80), nullable=False)
    upvotes = db.Column(ARRAY(db.Integer), default=list)
    resolver = db.Column(ARRAY(db.Integer), default=list, nullable=False)

    # Relationship to Comment
    comments = db.relationship('Comment', backref='complaint', cascade="all, delete-orphan")

    def json(self):
        return {
            'c_id': self.c_id,
            'user_id': self.user_id, 
            'message': self.complaint_message,
            'upvotes': self.upvotes,
            'resolver': self.resolver
        }

# Comment Model 
class Comment(db.Model):
    __tablename__ = 'comments'
    
    user_id = db.Column(db.String, nullable=False)
    comment_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    c_id = db.Column(db.String, db.ForeignKey('complaint.c_id'), nullable=False)  # Foreign key to Complaint
    comment_message = db.Column(db.String(120), nullable=False)

    def json(self):
        return {'comment_id': self.comment_id, 'c_id': self.c_id, 'c_message': self.comment_message}

# Complaint Statistics Model
class ComplaintStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_created = db.Column(db.Integer, default=0)
    total_resolved = db.Column(db.Integer, default=0)
