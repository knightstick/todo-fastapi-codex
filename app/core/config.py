"""Application configuration settings."""

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Todo FastAPI"
    database_url: str = "sqlite:///./todo.db"


settings = Settings()
