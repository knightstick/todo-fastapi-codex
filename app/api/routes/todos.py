"""Todo item API routes."""

from typing import List

from fastapi import APIRouter, HTTPException, status

from app import crud
from app.schemas.todo import TodoCreate, TodoInDB, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[TodoInDB])
async def get_todos() -> List[TodoInDB]:
    return await crud.todo.list_todos()


@router.post("/", response_model=TodoInDB, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate) -> TodoInDB:
    return await crud.todo.create_todo(todo)


@router.get("/{todo_id}", response_model=TodoInDB)
async def read_todo(todo_id: int) -> TodoInDB:
    todo = await crud.todo.get_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoInDB)
async def update_todo(todo_id: int, todo: TodoUpdate) -> TodoInDB:
    updated = await crud.todo.update_todo(todo_id, todo)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return updated


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int) -> None:
    removed = await crud.todo.delete_todo(todo_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
