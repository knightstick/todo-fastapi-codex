"""SQLAlchemy table definition for todo items."""

import sqlalchemy

from app.db import metadata


todos = sqlalchemy.Table(
    "todos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("is_completed", sqlalchemy.Boolean, default=False, nullable=False),
)
