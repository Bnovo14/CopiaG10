from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.auth import model, service
from ..database.core import engine, get_db
from ..rate_limiting import limiter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register_user(register_request: model.RegisterPersonRequest, db: Session = Depends(get_db)) -> model.Person:
    return service.register_user(db=db, register_request=register_request)

@router.post("/token", response_model=model.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session = Depends(get_db)) -> model.Token:
    return service.login_for_access_token(form_data=form_data, db=db)
