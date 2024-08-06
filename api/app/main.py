from fastapi import FastAPI
from .routers import items
from .database import engine, Base
from .logging_config import setup_logging

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)