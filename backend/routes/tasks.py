# backend/routes/tasks.py
from flask import Blueprint, request, jsonify
import logging
from ..extensions import db  # Changed to relative import
from ..models.task import Task  # Changed to relative import
import dateutil.parser

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    logger.info("Getting all tasks")
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route('', methods=['POST'])
def create_task():
    """Create a new task."""
    logger.info("Creating new task")
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    if not data.get('title'):
        return jsonify({"error": "Title is required"}), 400
        
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

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID."""
    logger.info(f"Getting task with id: {task_id}")
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    return jsonify(task.to_dict())

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a specific task by ID."""
    logger.info(f"Updating task with id: {task_id}")
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    
    if data.get('title'):
        task.title = data['title']
    if data.get('description') is not None:  # Allow empty description
        task.description = data['description']
    if data.get('due_date'):
        try:
            task.due_date = dateutil.parser.isoparse(data['due_date'])
        except ValueError as e:
            return jsonify({"error": f"Invalid date format: {str(e)}"}), 400
    if 'completed' in data:
        task.completed = bool(data['completed'])
    
    try:
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating task: {str(e)}")
        return jsonify({"error": "Error updating task"}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a specific task by ID."""
    logger.info(f"Deleting task with id: {task_id}")
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting task: {str(e)}")
        return jsonify({"error": "Error deleting task"}), 500