"""Integration tests for todo list API endpoints using TestClient."""

from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from app.schemas.todo_list import ListInDB


def test_list_lifecycle(client: TestClient) -> None:
    """Exercise create/read/update/delete list operations end-to-end."""

    list_response = client.get("/lists/")
    assert list_response.status_code == 200
    assert list_response.json() == []
    TypeAdapter(list[ListInDB]).validate_python(list_response.json())

    list_payload = {"title": "Work"}
    create_response = client.post("/lists/", json=list_payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == list_payload["title"]
    ListInDB.model_validate(created)
    list_id = created["id"]

    read_response = client.get(f"/lists/{list_id}")
    assert read_response.status_code == 200
    assert read_response.json() == created
    ListInDB.model_validate(read_response.json())

    update_payload = {"title": "Personal"}
    update_response = client.put(f"/lists/{list_id}", json=update_payload)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == update_payload["title"]
    ListInDB.model_validate(updated)

    list_after_update = client.get("/lists/")
    assert list_after_update.status_code == 200
    assert list_after_update.json() == [updated]
    TypeAdapter(list[ListInDB]).validate_python(list_after_update.json())

    delete_response = client.delete(f"/lists/{list_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/lists/{list_id}")
    assert missing_response.status_code == 404


def test_missing_list_responses(client: TestClient) -> None:
    """Ensure nonexistent list operations return 404."""

    assert client.get("/lists/999").status_code == 404
    assert client.put("/lists/999", json={"title": "missing"}).status_code == 404
    assert client.delete("/lists/999").status_code == 404
