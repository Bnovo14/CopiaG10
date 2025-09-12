from pydantic import BaseModel, Field
import datetime


class AgendamentoRequest(BaseModel):
    startTime: datetime.datetime = Field(..., description="Data e hora de início do agendamento", example="2025-09-10T09:00:00")
    endTime: datetime.datetime = Field(..., description="Data e hora de término do agendamento", example="2025-09-10T10:00:00")

    class Config:
        schema_extra = {
            "example": {
                "aluno_id": 1,
                "curso_id": 2,
                "startTime": "2025-09-10T09:00:00",
                "endTime": "2025-09-10T10:00:00"
            }
        }


