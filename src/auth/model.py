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
    doing_tcc: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "email": "aluno@example.com",
                "password": "senha123",
                "confirm_password": "senha123",
                "matricula": 123456,
                "curso_id": 1,
                "semestre": 5,
                "doing_tcc": False
            }
        }
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    aluno_id: int
    email: EmailStr