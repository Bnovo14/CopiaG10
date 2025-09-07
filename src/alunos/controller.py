from fastapi import APIRouter, Depends, status
from . import model
from src.auth.model import TokenData
from src.auth import service as auth_service
from . import service as aluno_service

router = APIRouter(
    prefix="/aluno",
    tags=["aluno"],
)

@router.get("/aluno/current", status_code=status.HTTP_200_OK)
def get_current_aluno(token_data: TokenData = Depends(auth_service.get_current_user)):
    return {"aluno_id": token_data.aluno_id}

@router.get("/aluno/{aluno_id}", response_model=model.AlunoRegisterRequest, status_code=status.HTTP_200_OK)
def get_aluno(aluno_id: int, db=Depends(aluno_service.get_db)):
    return aluno_service.get_aluno(aluno_id, db)

@router.delete("/aluno/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aluno(aluno_id: int, db=Depends(aluno_service.get_db)):
    aluno_service.delete_aluno(aluno_id, db)
    return None

@router.post("/aluno", response_model=model.AlunoRegisterRequest, status_code=status.HTTP_201_CREATED)
def create_aluno(
    aluno: model.AlunoRegisterRequest,
    db=Depends(aluno_service.get_db),
    current_user=Depends(aluno_service.get_current_user)
):
    return aluno_service.create_aluno(aluno, db, current_user)


@router.put("/aluno/{aluno_id}", response_model=model.AlunoResponse, status_code=status.HTTP_200_OK)
def update_aluno(
    aluno_id: int,
    aluno: model.AlunoUpdate,
    db=Depends(aluno_service.get_db),
):
    return aluno_service.update_aluno(aluno_id, aluno, db)