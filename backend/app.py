# backend/app.py - Application entry point
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime
import dateutil.parser  # We'll need to install python-dateutil

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pyboot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class Task(db.Model):
    """Task model for storing task-related data."""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """Convert task to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed
        }

@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    """Handle tasks endpoints."""
    logger.info(f"Tasks endpoint accessed with method: {request.method}")
    
    if request.method == 'GET':
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])
    
    if request.method == 'POST':
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        if not data.get('title'):
            return jsonify({"error": "Title is required"}), 400
            
        # Convert ISO format date string to Python datetime
        due_date = None
        if data.get('due_date'):
            try:
                due_date = dateutil.parser.isoparse(data['due_date'])
            except ValueError as e:
                return jsonify({"error": f"Invalid date format: {str(e)}"}), 400
            
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            due_date=due_date
        )
        
        try:
            db.session.add(task)
            db.session.commit()
            return jsonify(task.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating task: {str(e)}")
            return jsonify({"error": "Error creating task"}), 500

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)