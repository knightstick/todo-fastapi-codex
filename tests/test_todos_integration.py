"""Integration tests for todo API endpoints using TestClient."""

from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from app.schemas.todo import TodoInDB


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
