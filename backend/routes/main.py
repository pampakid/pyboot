# backend/routes/main.py - Basic routes
from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Home endpoint."""
    return jsonify({'message': 'Welcome to Pyboot API!'})

@main_bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})