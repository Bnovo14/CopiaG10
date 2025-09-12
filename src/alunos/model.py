from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class AlunoRegisterRequest(BaseModel):
    #aluno_id: UUID
    matricula: int
    curso_id: int
    semestre: int
    doing_tcc: bool
    email: EmailStr
    password: str
    confirm_password: str

class ChangePasswordRequest(BaseModel):
    aluno_id: int
    email: EmailStr
    old_password: str
    new_password: str

class AlunoResponse(BaseModel):
    aluno_id: int
    matricula: int
    curso_id: int
    semestre: int
    email: EmailStr
    active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class AlunoUpdate(BaseModel):
    matricula: Optional[int] = None
    curso_id: Optional[int] = None
    semestre: Optional[int] = None
    doing_tcc: Optional[bool] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None
