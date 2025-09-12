from sqlmodel import SQLModel, Field, Relationship
import datetime

class AgendamentoSuplente(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    agendamento_id: int = Field(foreign_key="agendamento.id")
    aluno_id: int = Field()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=None, sa_column_kwargs={"onupdate": datetime.datetime.utcnow}, nullable=True)