import logging
from fastapi import FastAPI
from database.core import engine
from sqlmodel import SQLModel

try:
    SQLModel.metadata.create_all(engine)
except Exception as e:
    logging.error(f"Error creating database tables: {e}")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
