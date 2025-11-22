"""CRUD helpers for todo items."""

from typing import List, Optional

from app.db import database
from app.models.todo import todos
from app.schemas.todo import TodoCreate, TodoInDB, TodoUpdate


async def list_todos() -> List[TodoInDB]:
    query = todos.select()
    rows = await database.fetch_all(query)
    return [TodoInDB(**row) for row in rows]


async def get_todo(todo_id: int) -> Optional[TodoInDB]:
    query = todos.select().where(todos.c.id == todo_id)
    row = await database.fetch_one(query)
    return TodoInDB(**row) if row else None


async def create_todo(todo: TodoCreate) -> TodoInDB:
    query = todos.insert().values(
        title=todo.title,
        description=todo.description,
        is_completed=todo.is_completed,
    )
    todo_id = await database.execute(query)
    return TodoInDB(id=todo_id, **todo.model_dump())


async def update_todo(todo_id: int, todo: TodoUpdate) -> Optional[TodoInDB]:
    existing = await get_todo(todo_id)
    if existing is None:
        return None

    update_data = todo.model_dump(exclude_unset=True)
    query = (
        todos.update()
        .where(todos.c.id == todo_id)
        .values(**update_data)
    )
    await database.execute(query)
    return await get_todo(todo_id)


async def delete_todo(todo_id: int) -> bool:
    query = todos.delete().where(todos.c.id == todo_id)
    result = await database.execute(query)
    return bool(result)
