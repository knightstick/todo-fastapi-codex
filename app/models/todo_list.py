"""SQLAlchemy table definition for todo lists."""

import sqlalchemy

from app.db import metadata


todo_lists = sqlalchemy.Table(
    "todo_lists",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
)
