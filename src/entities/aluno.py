import datetime
from sqlmodel import SQLModel, Field

class Aluno(SQLModel, table=True):
    aluno_id: int = Field(default=None, primary_key=True)
    matricula: str = Field(default=None)
    email: str = Field(default=None)
    curso_id: int = Field(foreign_key="curso.id", default=None)
    semestre: int = Field(default=None)
    doing_tcc: bool = Field(default=False)
    password_hash: str = Field(default=None)
    active: bool = Field(default=True)
    created_at: datetime = Field(default= datetime.datetime.utcnow())
    updated_at: datetime = Field(default= None, nullable=True)

