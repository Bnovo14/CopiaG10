import logging
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.database.core import engine
from sqlmodel import SQLModel
from src.auth.controller import router as auth_router
from src.alunos.controller import router as aluno_router
from src.agendamentos.controller import router as agendamento_router
from fastapi.openapi.utils import get_openapi
# Importando todos os modelos de entidades
from src.entities.curso import Curso
from src.entities.aluno import Aluno
from src.entities.agendamento import Agendamento

def init_db():
    try:
        logging.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        logging.info("Database tables created successfully!")
    except Exception as e:
        logging.error(f"Failed to create database tables: {str(e)}")
        raise

# Initialize the database
init_db()

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Projeto do Sistema de Agendamento para a Máquina de Corte para FAU",
        version="1.0.0",
        routes=app.routes,
    )
    
    # Adiciona a versão do OpenAPI
    openapi_schema["openapi"] = "3.0.2"
    
    # Adiciona apenas o securitySchemes, mantendo os schemas automáticos
    openapi_schema.setdefault("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(aluno_router)
router.include_router(agendamento_router)

app.include_router(router)

# Configurar schema OpenAPI customizado
app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
