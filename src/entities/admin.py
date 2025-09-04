from sqlmodel import SQLModel, Field

class Admin(SQLModel, table=True):
    admin_id: int = Field(default=None, primary_key=True)
    email: str = Field(default=None)
    password_hash: str = Field(default=None)
    active: bool = Field(default=True)
