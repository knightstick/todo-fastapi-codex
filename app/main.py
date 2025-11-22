"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app import crud
from app.api.routes.todos import router as todos_router
from app.core.config import settings
from app.db import database, engine, metadata


metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name)
app.include_router(todos_router)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


__all__ = ["app", "crud"]
