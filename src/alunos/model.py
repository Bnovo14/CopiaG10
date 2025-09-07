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
    created_at: datetime
    updated_at: datetime

class AlunoUpdate(BaseModel):
    matricula: int | None = None
    curso_id: int | None = None
    semestre: int | None = None
    doing_tcc: bool | None = None
    email: EmailStr | None = None
    active: bool | None = None
