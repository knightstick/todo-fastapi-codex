"""Integration tests for todo API endpoints using TestClient."""

import importlib
import sys
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from pydantic import TypeAdapter


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core import config
from app.schemas.todo import TodoInDB


@pytest.fixture()
def client(tmp_path, monkeypatch) -> Iterator[TestClient]:
    """Provide a TestClient wired to an isolated SQLite database."""

    test_db = tmp_path / "test.db"
    db_url = f"sqlite:///{test_db}"
    monkeypatch.setattr(config.settings, "database_url", db_url)

    # Reload modules to bind to the test database URL.
    import app.db as db
    import app.models.todo as models
    import app.crud.todo as crud_todo
    import app.crud as crud_pkg
    import app.api.routes.todos as routes
    import app.main as main

    importlib.reload(db)
    importlib.reload(models)
    importlib.reload(crud_todo)
    importlib.reload(crud_pkg)
    importlib.reload(routes)
    main = importlib.reload(main)

    with TestClient(main.app) as client:
        yield client


def test_todo_lifecycle(client: TestClient) -> None:
    """Exercise create/read/update/delete todo operations end-to-end."""

    # Start with an empty collection.
    list_response = client.get("/todos/")
    assert list_response.status_code == 200
    assert list_response.json() == []
    TypeAdapter(list[TodoInDB]).validate_python(list_response.json())

    # Create a new todo item.
    todo_payload = {
        "title": "Write tests",
        "description": "Add integration coverage",
        "is_completed": False,
    }
    create_response = client.post("/todos/", json=todo_payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == todo_payload["title"]
    assert created["description"] == todo_payload["description"]
    assert created["is_completed"] is todo_payload["is_completed"]
    TodoInDB.model_validate(created)
    todo_id = created["id"]

    # Retrieve the created item.
    read_response = client.get(f"/todos/{todo_id}")
    assert read_response.status_code == 200
    assert read_response.json() == created
    TodoInDB.model_validate(read_response.json())

    # Update the todo entry.
    update_payload = {"title": "Write more tests", "is_completed": True}
    update_response = client.put(f"/todos/{todo_id}", json=update_payload)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == update_payload["title"]
    assert updated["description"] == todo_payload["description"]
    assert updated["is_completed"] is True
    TodoInDB.model_validate(updated)

    # Verify listing reflects the updated item.
    list_after_update = client.get("/todos/")
    assert list_after_update.status_code == 200
    assert list_after_update.json() == [updated]
    TypeAdapter(list[TodoInDB]).validate_python(list_after_update.json())

    # Delete the todo and ensure it's gone.
    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/todos/{todo_id}")
    assert missing_response.status_code == 404


def test_missing_todo_responses(client: TestClient) -> None:
    """Ensure nonexistent todo operations return 404."""

    assert client.get("/todos/999").status_code == 404
    assert client.put("/todos/999", json={"title": "missing"}).status_code == 404
    assert client.delete("/todos/999").status_code == 404
