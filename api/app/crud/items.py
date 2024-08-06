from sqlalchemy.orm import Session
from ..models.items import Item
from ..schemas.items import ItemCreate, ItemUpdate


def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int):
    return db.query(Item).filter(item_id == Item.id).first()


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()


def update_item(db: Session, item_id: int, item: ItemUpdate):
    db_item = db.query(Item).filter(item_id == Item.id).first()
    if db_item:
        for key, value in item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(item_id == Item.id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
