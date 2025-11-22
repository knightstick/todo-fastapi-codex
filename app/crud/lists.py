"""CRUD helpers for todo lists."""

from typing import List, Optional

from app.db import database
from app.models.todo_list import todo_lists
from app.schemas.todo_list import ListCreate, ListInDB, ListUpdate


async def list_lists() -> List[ListInDB]:
    query = todo_lists.select()
    rows = await database.fetch_all(query)
    return [ListInDB(**row) for row in rows]


async def get_list(list_id: int) -> Optional[ListInDB]:
    query = todo_lists.select().where(todo_lists.c.id == list_id)
    row = await database.fetch_one(query)
    return ListInDB(**row) if row else None


async def create_list(todo_list: ListCreate) -> ListInDB:
    query = todo_lists.insert().values(title=todo_list.title)
    list_id = await database.execute(query)
    return ListInDB(id=list_id, **todo_list.model_dump())


async def update_list(list_id: int, todo_list: ListUpdate) -> Optional[ListInDB]:
    existing = await get_list(list_id)
    if existing is None:
        return None

    update_data = todo_list.model_dump(exclude_unset=True)
    query = todo_lists.update().where(todo_lists.c.id == list_id).values(**update_data)
    await database.execute(query)
    return await get_list(list_id)


async def delete_list(list_id: int) -> bool:
    query = todo_lists.delete().where(todo_lists.c.id == list_id)
    result = await database.execute(query)
    return bool(result)
