from sqlmodel import SQLModel, Field, Relationship 

class AgendamentoStatus(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True, unique=True)