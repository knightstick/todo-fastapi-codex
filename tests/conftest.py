"""Shared test fixtures."""

import importlib
import sys
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _reload_app_modules() -> TestClient:
    """Reload application modules to bind to the patched database URL."""

    import app.db as db
    import app.models.todo_list as list_models
    import app.models.todo as todo_models
    import app.crud.lists as crud_list
    import app.crud.todo as crud_todo
    import app.crud as crud_pkg
    import app.api.routes.lists as list_routes
    import app.api.routes.todos as todo_routes
    import app.main as main

    importlib.reload(db)
    importlib.reload(list_models)
    importlib.reload(todo_models)
    importlib.reload(crud_list)
    importlib.reload(crud_todo)
    importlib.reload(crud_pkg)
    importlib.reload(list_routes)
    importlib.reload(todo_routes)
    main = importlib.reload(main)

    return main.app


@pytest.fixture()
def client(tmp_path, monkeypatch) -> Iterator[TestClient]:
    """Provide a TestClient wired to an isolated SQLite database."""

    test_db = tmp_path / "test.db"
    db_url = f"sqlite:///{test_db}"
    from app.core import config

    monkeypatch.setattr(config.settings, "database_url", db_url)

    app = _reload_app_modules()
    with TestClient(app) as test_client:
        yield test_client
