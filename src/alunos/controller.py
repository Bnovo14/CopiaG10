from fastapi import APIRouter, Depends, Request
from src.database.core import get_db
from sqlmodel import Session, update
from exceptions import NotFoundException
from . import model
from entities import entity
from src.auth import service as auth_service

router = APIRouter(
    prefix="/aluno",
    tags=["aluno"],
)

@router.get("/aluno/{aluno_id}", response_model=model.AlunoRegisterRequest)
def get_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(entity.Aluno).filter(entity.Aluno.aluno_id == aluno_id).first()
    if not aluno:
        raise NotFoundException("Aluno não encontrado")
    return aluno

@router.delete("/aluno/{aluno_id}")
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(entity.Aluno).filter(entity.Aluno.aluno_id == aluno_id).first()
    if not aluno:
        raise NotFoundException("Aluno não encontrado")
    stmt = update(aluno).values(active=False)
    db.execute(stmt)
    db.commit()
    return {"message": "Aluno deletado com sucesso"}



@router.get("/aluno/current")
def get_current_aluno(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise NotFoundException("Token de autenticação não fornecido")
    token = auth_header.split(" ", 1)[1]
    user = auth_service.get_current_user(token)
    return {"aluno_id": user.aluno_id}

@router.post("/aluno", response_model=model.AlunoRegisterRequest)
def create_aluno(aluno: model.AlunoRegisterRequest, db: Session = Depends(get_db)):
    # Chama o método de cadastro do auth
    novo_aluno = auth_service.register_user(db, aluno)
    return novo_aluno