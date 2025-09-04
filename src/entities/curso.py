from sqlmodel import SQLModel, Field

class Curso(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(default=None)
    duracao: int = Field(default=None)
