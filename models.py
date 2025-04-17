from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

# Create db instance without app
db = SQLAlchemy()

# Complaint Model
class Complaint(db.Model):
    __tablename__ = 'complaint'
    
    c_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    c_message = db.Column(db.String(80), nullable=False)
    upvotes = db.Column(ARRAY(db.Integer), default=list)
    resolver = db.Column(ARRAY(db.Integer), default=list, nullable=False)

    # Relationship to Comment
    comments = db.relationship('Comment', backref='complaint', cascade="all, delete-orphan")

    def json(self):
        return {
            'c_id': self.c_id,
            'user_id': self.user_id, 
            'message': self.c_message,
            'upvotes': self.upvotes,
            'resolver': self.resolver
        }

# Comment Model
class Comment(db.Model):
    __tablename__ = 'comments'
    
    user_id = db.Column(db.Integer, nullable=False)
    comment_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, db.ForeignKey('complaint.c_id'), nullable=False)  # Foreign key to Complaint
    c_message = db.Column(db.String(120), nullable=False)

    def json(self):
        return {'comment_id': self.comment_id, 'c_id': self.c_id, 'c_message': self.c_message}