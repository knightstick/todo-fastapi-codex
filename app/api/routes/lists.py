"""Todo list API routes."""

from typing import List

from fastapi import APIRouter, HTTPException, status

from app import crud
from app.schemas.todo_list import ListCreate, ListInDB, ListUpdate

router = APIRouter(prefix="/lists", tags=["lists"])


@router.get("/", response_model=List[ListInDB])
async def get_lists() -> List[ListInDB]:
    return await crud.lists.list_lists()


@router.post("/", response_model=ListInDB, status_code=status.HTTP_201_CREATED)
async def create_list(todo_list: ListCreate) -> ListInDB:
    return await crud.lists.create_list(todo_list)


@router.get("/{list_id}", response_model=ListInDB)
async def read_list(list_id: int) -> ListInDB:
    todo_list = await crud.lists.get_list(list_id)
    if todo_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    return todo_list


@router.put("/{list_id}", response_model=ListInDB)
async def update_list(list_id: int, todo_list: ListUpdate) -> ListInDB:
    updated = await crud.lists.update_list(list_id, todo_list)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    return updated


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(list_id: int) -> None:
    removed = await crud.lists.delete_list(list_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
