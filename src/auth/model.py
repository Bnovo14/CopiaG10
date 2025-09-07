from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    username: str 
    password: str

class RegisterAlunoRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    matricula: int
    curso_id: int
    semestre: int
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    aluno_id: int
    email: EmailStr