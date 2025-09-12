from fastapi import APIRouter, Depends
import src.agendamentos.service as service
from src.agendamentos.model import AgendamentoRequest
from src.database.core import get_db
from sqlmodel import Session
from src.exceptions import NotFoundException
from src.alunos.service import get_current_user

router = APIRouter(prefix="/agendamentos",
                   tags=["Agendamentos"])

@router.get("/")
def list_agendamentos(db: Session = Depends(get_db)):
    return service.list_agendamentos(db)

@router.post("/")
def create_agendamento(
    agendamento_request: AgendamentoRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return service.create_agendamento(db, agendamento_request, current_user)

@router.get("/{agendamento_id}")
def get_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = service.get_agendamento(db, agendamento_id)
    if not agendamento:
        raise NotFoundException("Agendamento não encontrado")
    return agendamento

@router.delete("/{agendamento_id}")
def delete_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    success = service.delete_agendamento(db, agendamento_id)
    if not success:
        raise NotFoundException("Agendamento não encontrado")
    return {"message": "Agendamento cancelado com sucesso"}