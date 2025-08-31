from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class AlunoRegisterRequest(BaseModel):
    #aluno_id: UUID
    matricula: int
    curso_id: UUID
    semestre: int
    doing_tcc: bool
    
