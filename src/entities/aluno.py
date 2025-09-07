from datetime import datetime
from sqlmodel import SQLModel, Field

class Aluno(SQLModel, table=True):
    aluno_id: int = Field(default=None, primary_key=True)
    matricula: str = Field(default=None)
    email: str = Field(default=None)
    curso_id: int = Field(default=None)
    semestre: int = Field(default=None)
    doing_tcc: bool = Field(default=False)
    password_hash: str = Field(default=None)
    active: bool = Field(default=True)
    admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default=None, nullable=True)

    model_config = {
        "arbitrary_types_allowed": True
    }

