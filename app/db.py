"""Database configuration and metadata."""

import sqlalchemy
from databases import Database

from app.core.config import settings


metadata = sqlalchemy.MetaData()
database = Database(settings.database_url)
engine = sqlalchemy.create_engine(settings.database_url, connect_args={"check_same_thread": False})
