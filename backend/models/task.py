# backend/models/task.py
from datetime import datetime
from ..app import db

class Task(db.Model):
    """Task model for storing task-related data"""
    __tablename__ = 'tasks'

    id = db.Colum(db.Integer, primary_key=True)
    title = db.Column(sb.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Return string representation of the task"""
        return f'<Task {self.title}>'
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed
        }