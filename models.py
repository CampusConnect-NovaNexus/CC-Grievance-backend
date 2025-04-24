from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import uuid
from datetime import datetime, timezone

db = SQLAlchemy()

# Complaint Model
class Complaint(db.Model):
    __tablename__ = 'complaint'

    user_id = db.Column(db.String, nullable=False)
    c_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4())) 
    complaint_title = db.Column(db.String(30), nullable=False)
    complaint_message = db.Column(db.String(120), nullable=False)
    upvotes = db.Column(ARRAY(db.Integer), default=list)
    resolver = db.Column(ARRAY(db.Integer), default=list, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  

    # Relationship to Comment
    comments = db.relationship('Comment', backref='complaint', cascade="all, delete-orphan")

    def json(self):
        return {
            'c_id': self.c_id,
            'user_id': self.user_id, 
            'message': self.complaint_message,
            'upvotes': self.upvotes,
            'resolver': self.resolver,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Comment Model 
class Comment(db.Model):
    __tablename__ = 'comments'
    
    user_id = db.Column(db.String, nullable=False)
    comment_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    c_id = db.Column(db.String, db.ForeignKey('complaint.c_id'), nullable=False)
    comment_message = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 

    def json(self):
        return {
            'comment_id': self.comment_id,
            'c_id': self.c_id,
            'c_message': self.comment_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Complaint Statistics Model
class ComplaintStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_created = db.Column(db.Integer, default=0)
    total_resolved = db.Column(db.Integer, default=0)