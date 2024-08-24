from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import items, auth
from app.database import engine, Base
from app.logging_config import setup_logging

# Set up logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="todo application",
    description="Welcome, this is my todo application. Authenticate to be able to use this API",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Change this to your frontend’s URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items.router, prefix="/api", tags=["items"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
