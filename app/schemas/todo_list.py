"""Pydantic models for todo lists."""

from pydantic import BaseModel


class ListBase(BaseModel):
    title: str


class ListCreate(ListBase):
    pass


class ListUpdate(BaseModel):
    title: str | None = None


class ListInDB(ListBase):
    id: int

    class Config:
        from_attributes = True
