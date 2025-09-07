from fastapi import Request
from sqlmodel import Session
from fastapi import Depends, HTTPException
from src.database.core import get_db
from . import model
from src.exceptions import NoAccessException, NotFoundException
import src.log_config
from src.auth import service as auth_service
from sqlmodel import Session, update
from src.entities.aluno import Aluno


def get_current_user(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise NoAccessException("Faça login para acessar este recurso")
    token = auth_header.split(" ", 1)[1]
    user = auth_service.get_current_user(token)
    return user

def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.aluno_id == aluno_id).first()
    if not aluno:
        raise NotFoundException("Aluno não encontrado")
    stmt = update(Aluno).where(Aluno.aluno_id == aluno_id).values(active=False)
    db.execute(stmt)
    db.commit()
    return {"message": "Aluno deletado com sucesso"}

def get_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.aluno_id == aluno_id).first()
    if not aluno:
        raise NotFoundException("Aluno não encontrado")
    return aluno

def create_aluno(
    aluno: model.AlunoRegisterRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    novo_aluno = auth_service.register_user(db, aluno)
    return novo_aluno

def update_aluno(
        aluno_id:int,
        aluno: model.AlunoUpdate,
        db: Session = Depends(get_db)
):
    current_id = get_current_user()
    current_user = db.query(Aluno).filter(Aluno.aluno_id == current_id.aluno_id).first()
    if current_id.aluno_id != aluno_id and not current_user.admin:
        raise NoAccessException("Você não tem permissão para atualizar este aluno")
    aluno_to_update = db.query(Aluno).filter(Aluno.aluno_id == aluno_id).first()
    if not aluno_to_update:
        raise NotFoundException("Aluno não encontrado")
    for key, value in aluno.dict(exclude_unset=True).items():
        setattr(aluno_to_update, key, value)
    db.commit()
    return aluno_to_update