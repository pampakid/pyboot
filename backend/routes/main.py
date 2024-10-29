# backend/routes/main.py - Basic routes
from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return jsonify({'message': 'Welcome to Pyboot API'})

@bp.route('/health')
def health():
    return jsonify({'status': 'healthy'})