# backend/routes/tasks.py
from flask import Blueprint, request, jsonify
from backend.models.task import Task
from backend.extensions import db

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route('/', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
        
    task = Task(
        title=data.get('title'),
        description=data.get('description'),
        due_date=data.get('due_date')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task."""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task."""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.completed = data.get('completed', task.completed)
    
    db.session.commit()
    
    return jsonify(task.to_dict())

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    return '', 204