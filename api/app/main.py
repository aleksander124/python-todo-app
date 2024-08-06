from fastapi import FastAPI
from routers import items, auth
from database import engine, Base
from logging_config import setup_logging

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="todo application",
    description="Welcome this is my todo application. Authenticate to be able to use this api",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(items.router, prefix="/api")
app.include_router(auth.router, prefix="/auth", tags=["auth"])


