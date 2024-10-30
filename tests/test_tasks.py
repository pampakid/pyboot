# backend/tests/test_tasks.py
import pytest
from datetime import datetime, UTC
from backend.models.task import Task

def test_cors_headers(client):
    """Test that CORS headers are present."""
    response = client.get('/api/tasks')
    assert 'Access-Control-Allow-Origin' in response.headers

def test_get_all_tasks_empty(client, db_session):
    """Test getting all tasks when database is empty."""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert response.json == []

def test_create_task(client, db_session):
    """Test creating a new task."""
    task_data = {
        'title': 'New Task',
        'description': 'New Description',
        'due_date': '2024-12-01T00:00:00Z'
    }
    response = client.post('/api/tasks',
                          json=task_data)
    assert response.status_code == 201
    assert response.json['title'] == 'New Task'
    assert response.json['description'] == 'New Description'
    assert not response.json['completed']

def test_get_task_detail(client, sample_task):
    """Test getting a single task."""
    response = client.get(f'/api/tasks/{sample_task.id}')
    assert response.status_code == 200
    assert response.json['title'] == 'Test Task'
    assert response.json['description'] == 'Test Description'

def test_update_task(client, sample_task):
    """Test updating a task."""
    update_data = {
        'title': 'Updated Task',
        'completed': True
    }
    response = client.put(f'/api/tasks/{sample_task.id}',
                         json=update_data)
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Task'
    assert response.json['completed']

def test_delete_task(client, sample_task):
    """Test deleting a task."""
    response = client.delete(f'/api/tasks/{sample_task.id}')
    assert response.status_code == 204
    # Verify task is deleted
    get_response = client.get(f'/api/tasks/{sample_task.id}')
    assert get_response.status_code == 404

def test_task_not_found(client):
    """Test requesting a non-existent task."""
    response = client.get('/api/tasks/999')
    assert response.status_code == 404
    assert 'error' in response.json