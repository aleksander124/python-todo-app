import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.items import create_item as crud_create_item, get_item as crud_get_item, get_items as crud_get_items, delete_item as crud_delete_item, update_item as crud_update_item
from schemas.items import ItemCreate, ItemUpdate, Item
from dependencies import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/items/", response_model=Item)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db)):
    logger.info("Creating item", extra={"item": item.dict()})
    return crud_create_item(db=db, item=item)


@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching item with id {item_id}")
    db_item = crud_get_item(db, item_id=item_id)
    if db_item is None:
        logger.error("Item not found", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/items/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching items with skip={skip} and limit={limit}")
    items = crud_get_items(db, skip=skip, limit=limit)
    return items


@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating item with id {item_id}", extra={"item_update": item.dict()})
    db_item = crud_update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        logger.error("Item not found for update", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting item with id {item_id}")
    db_item = crud_delete_item(db=db, item_id=item_id)
    if db_item is None:
        logger.error("Item not found for deletion", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
