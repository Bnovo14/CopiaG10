from src.agendamentos.model import AgendamentoRequest
from src.entities.agendamento import Agendamento
from src.alunos.service import get_aluno, get_current_user
from fastapi import Body
from src.exceptions import NotFoundException
import datetime

def create_agendamento(db_session, agendamento_request: AgendamentoRequest, current_user):
    aluno = get_aluno(db_session, current_user.aluno_id)
    if not aluno:
        raise NotFoundException("Aluno não encontrado")
    if agendamento_request.startTime >= agendamento_request.endTime:
        raise ValueError("A data de início deve ser anterior à data de término")
    if agendamento_request.startTime < datetime.datetime.now():
        raise ValueError("A data de início não pode ser no passado")
    
    agendamento = Agendamento(**agendamento_request.dict(), aluno_id=current_user.aluno_id, curso_id=aluno.curso_id)
    db_session.add(agendamento)
    db_session.commit()
    db_session.refresh(agendamento)
    return agendamento

def get_agendamento(db_session, agendamento_id: int):
    return db_session.get(Agendamento, agendamento_id)

def list_agendamentos(db_session):
    return db_session.query(Agendamento).all()

def delete_agendamento(db_session, agendamento_id: int):
    agendamento = get_agendamento(db_session, agendamento_id)
    if agendamento:
        agendamento.status = 1  
        db_session.add(agendamento)
        db_session.commit()
        db_session.refresh(agendamento)
        return True
    return False

def update_agendamento(db_session, agendamento_id: int, agendamento_request: AgendamentoRequest):
    agendamento = get_agendamento(db_session, agendamento_id)
    if agendamento:
        for key, value in agendamento_request.dict().items():
            setattr(agendamento, key, value)
        db_session.add(agendamento)
        db_session.commit()
        db_session.refresh(agendamento)
        return agendamento
    return None