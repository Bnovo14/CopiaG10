import logging
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.database.core import engine
from sqlmodel import SQLModel
from src.auth.controller import router as auth_router
from src.alunos.controller import router as aluno_router
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

# Criar router principal para versão da API
api_v1 = APIRouter(prefix="/api/v1")

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
    
    # Adiciona os schemas
    from src.auth.model import RegisterAlunoRequest, LoginRequest, Token
    
    openapi_schema["components"] = {
        "schemas": {
            "RegisterAlunoRequest": {
                "title": "RegisterAlunoRequest",
                "type": "object",
                "required": ["email", "password", "confirm_password", "matricula", "curso_id", "semestre"],
                "properties": {
                    "email": {"title": "Email", "type": "string", "format": "email"},
                    "password": {"title": "Password", "type": "string"},
                    "confirm_password": {"title": "Confirm Password", "type": "string"},
                    "matricula": {"title": "Matricula", "type": "integer"},
                    "curso_id": {"title": "Curso ID", "type": "integer"},
                    "semestre": {"title": "Semestre", "type": "integer"},
                    "doing_tcc": {"title": "Doing TCC", "type": "boolean", "default": False}
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "type": "object",
                "required": ["loc", "msg", "type"],
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "integer"}
                            ]
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            }
        },
        "securitySchemes": {
            "Bearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    }
    openapi_schema["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(aluno_router)
# Incluir routers na versão v1 da API
api_v1.include_router(auth_router)
api_v1.include_router(aluno_router)

# Incluir router v1 no app principal
app.include_router(api_v1)

# Configurar schema OpenAPI customizado
app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
