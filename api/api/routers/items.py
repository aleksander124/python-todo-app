import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, dependencies

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(dependencies.get_db)):
    logger.info("Creating item", extra={"item": item.dict()})
    return crud.items.create_item(db=db, item=item)


@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(dependencies.get_db)):
    logger.info(f"Fetching item with id {item_id}")
    db_item = crud.items.get_item(db, item_id=item_id)
    if db_item is None:
        logger.error("Item not found", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    logger.info(f"Fetching items with skip={skip} and limit={limit}")
    items = crud.items.get_items(db, skip=skip, limit=limit)
    return items


@router.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(dependencies.get_db)):
    logger.info(f"Updating item with id {item_id}", extra={"item_update": item.dict()})
    db_item = crud.items.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        logger.error("Item not found for update", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(dependencies.get_db)):
    logger.info(f"Deleting item with id {item_id}")
    db_item = crud.items.delete_item(db=db, item_id=item_id)
    if db_item is None:
        logger.error("Item not found for deletion", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
