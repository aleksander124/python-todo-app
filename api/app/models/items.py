from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Ensure 'title' matches 'name' in schema
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)