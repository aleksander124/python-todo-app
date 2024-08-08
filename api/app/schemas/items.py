from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True