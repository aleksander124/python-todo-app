from sqlalchemy.orm import Session
from app.models.items import Item
from app.schemas.items import ItemCreate, ItemUpdate


def create_item(db: Session, item: ItemCreate, creator_id: int):
    # Add the creator_id to the item
    db_item = Item(**item.dict(), creator_id=creator_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


#TODO: add function to get_user_items
def get_item(db: Session, item_id: int):
    return db.query(Item).filter(item_id == Item.id).first()


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()


def get_current_user_items(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Item).filter(Item.creator_id == user_id).offset(skip).limit(limit).all()


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
