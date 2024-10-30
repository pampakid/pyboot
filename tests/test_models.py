# backend/tests/test_models.py
import pytest
from datetime import datetime, UTC
from backend.models.task import Task

def test_task_model_creation(db_session):
    """Test Task model creation and defaults."""
    task = Task(
        title="Test Task",
        description="Test Description",
        due_date=datetime(2024, 12, 1, tzinfo=UTC)
    )
    db_session.session.add(task)
    db_session.session.commit()

    assert task.id is not None
    assert task.title == "Test Task"
    assert not task.completed
    assert task.created_at is not None

def test_task_model_validation(db_session):
    """Test Task model validation."""
    # Test missing required field
    task = Task(description="No Title")
    db_session.session.add(task)
    with pytest.raises(Exception):  # Adjust exception type based on your validation
        db_session.session.commit()