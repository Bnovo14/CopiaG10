from uuid import UUID
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

#Modificar posteriormente
class Person(SQLModel, table=True):
    id: UUID | None = Field(default=None, primary_key=True)
    email: EmailStr
    name: str
    hashed_password: str
