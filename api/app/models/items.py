from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Ensure 'title' matches 'name' in schema
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="items")