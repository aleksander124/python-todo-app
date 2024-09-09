import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.items import create_item as crud_create_item, get_item as crud_get_item, get_items as crud_get_items
from app.crud.items import delete_item as crud_delete_item, update_item as crud_update_item, get_current_user_items
from app.schemas.items import ItemCreate, ItemUpdate, Item
from app.dependencies.db_connect import get_db
from app.dependencies.auth import get_current_user
from app.models import User

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/items/", response_model=Item)
def create_item_endpoint(
        item: ItemCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # Get the current authenticated user
):
    # Automatically assign the creator (current user) to the item
    logger.info("Creating item", extra={"item": item.dict(), "creator_id": current_user.id})

    # Add creator_id to the item
    db_item = crud_create_item(db=db, item=item, creator_id=current_user.id)
    return db_item


@router.get("/items/{item_id}", response_model=Item)
def read_item(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # Require authentication
):
    logger.info(f"Fetching item with id {item_id}")

    # Ensure the current user is authenticated
    if not current_user:
        logger.error("Unauthorized access to item", extra={"item_id": item_id})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    db_item = crud_get_item(db, item_id=item_id)
    if db_item is None:
        logger.error("Item not found", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item


@router.get("/items/", response_model=list[Item])
def read_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Require authentication
):
    logger.info(f"Fetching items with skip={skip} and limit={limit}")

    # Ensure the current user is authenticated
    if not current_user:
        logger.error("Unauthorized access to items list")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    items = crud_get_items(db, skip=skip, limit=limit)
    return items


@router.get("/my/items", response_model=List[Item], description="Retrieve current user's items.")
def get_my_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_current_user_items(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.put("/items/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Updating item with id {item_id}", extra={"item_update": item.dict()})

    # Ensure the current user is authenticated
    if not current_user:
        logger.error("Unauthorized user tried to update item", extra={"item_id": item_id})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Optionally, you could check if the current user owns the item
    db_item = crud_update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        logger.error("Item not found for update", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item


@router.delete("/items/{item_id}", response_model=Item)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Require authentication
):
    logger.info(f"Deleting item with id {item_id}")

    # Ensure the current user is authenticated
    if not current_user:
        logger.error("Unauthorized access to delete item", extra={"item_id": item_id})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    db_item = crud_delete_item(db=db, item_id=item_id)
    if db_item is None:
        logger.error("Item not found for deletion", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item