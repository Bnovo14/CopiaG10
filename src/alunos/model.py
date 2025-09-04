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