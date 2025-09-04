import logging
from fastapi import APIRouter, FastAPI
from database.core import engine
from sqlmodel import SQLModel
from src.auth.controller import router as auth_router

try:
    SQLModel.metadata.create_all(engine)
except Exception as e:
    logging.error(f"Error creating database tables: {e}")

app = FastAPI()
router = APIRouter("/api/v1")
router.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
