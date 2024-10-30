# backend/tests/conftest.py
import pytest
from datetime import datetime, UTC
from backend.app import create_app
from backend.extensions import db
from backend.models.task import Task

@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'DEBUG': False
    })
    return app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Create database tables and provide a session."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_task(db_session):  # Fixed the fixture name from 'sambple_task'
    """Create a sample task for testing."""
    task = Task(
        title="Test Task",
        description="Test Description",
        due_date=datetime(2024, 12, 1, tzinfo=UTC),  # Using UTC instead of timezone.utc
        completed=False
    )
    db_session.session.add(task)
    db_session.session.commit()
    return task