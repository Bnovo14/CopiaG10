from dotenv import load_dotenv
from sqlmodel import Session, create_engine
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session