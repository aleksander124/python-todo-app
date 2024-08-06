from fastapi import FastAPI
from routers import items
from database import engine, Base
from logging_config import setup_logging

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="todo application",
    description="Welcome in todo application",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(items.router, prefix="/api")


