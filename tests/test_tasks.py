import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def test_task():
    """Фикстура для создания тестовой задачи."""
    return {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "in_progress",
    }


def test_create_task(test_task):
    """Тест на создание задачи."""
    response = client.post("/api/tasks/", json=test_task)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_task["title"]
    assert data["description"] == test_task["description"]
    assert data["status"] == test_task["status"]
    assert "id" in data


def test_get_tasks():
    """Тест на получение списка задач."""
    response = client.get("/api/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # Проверяем только если задачи уже существуют
        assert "title" in data[0]
        assert "description" in data[0]
        assert "status" in data[0]
