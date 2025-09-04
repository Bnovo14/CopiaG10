from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.auth import model, service
from src.alunos.controller import create_aluno
from ..database.core import engine, get_db
from ..rate_limiting import limiter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# @limiter.limit("5/minute") para limitar o número de registros (controle de DDoS)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(register_request: model.RegisterAlunoRequest, db: Session = Depends(get_db)):
    # Cria autenticação
    user = service.register_user(db=db, register_request=register_request)
    # Cria aluno
    aluno_data = {
        "matricula": register_request.matricula,
        "curso_id": register_request.curso_id,
        "semestre": register_request.semestre,
        "doing_tcc": getattr(register_request, "doing_tcc", False),
        "email": register_request.email,
        "password": register_request.password,
        "confirm_password": register_request.confirm_password
    }
    create_aluno(model.AlunoRegisterRequest(**aluno_data), db)
    return user

@router.post("/token", response_model=model.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session = Depends(get_db)) -> model.Token:
    return service.login_for_access_token(form_data=form_data, db=db)
