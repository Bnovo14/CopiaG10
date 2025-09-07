import datetime
from sqlmodel import SQLModel, Field, Relationship

class Agendamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    aluno_id: int = Field()
    curso_id: int = Field()
    startTime: datetime.datetime
    endTime: datetime.datetime
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, sa_column_kwargs={"onupdate": datetime.datetime.utcnow})
    status: str
    