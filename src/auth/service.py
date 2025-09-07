from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
import jwt
from src.entities.aluno import Aluno
from jwt import PyJWTError
from sqlmodel import Session
from . import model
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging
import os
from src.exceptions import InvalidTokenException

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def authenticate_user(email: str, password: str, db:Session) -> Aluno | None:
    user = db.query(Aluno).filter(Aluno.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Erro de autenticação no email: {email}")
        return False
    return user

def create_access_token(email: str, aluno_id: int, expires_delta: timedelta) -> str:
    to_encode = {"sub": email, "aluno_id": str(aluno_id), "exp": datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> model.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        aluno_id: str = payload.get("aluno_id")
        if email is None or aluno_id is None:
            raise AuthenticationError("Token inválido")
        return model.TokenData(aluno_id=int(aluno_id), email=email)
    except PyJWTError as e:
        logging.error(f"Erro ao decodificar o token: {e}")
        raise InvalidTokenException("Erro ao decodificar o token")

#Modificar posteriormente
def register_user(db: Session, register_request) -> Aluno:
    from src.entities.aluno import Aluno as AlunoEntity
    try:
        hashed_password = get_password_hash(register_request.password)
        new_user = AlunoEntity(
            matricula=register_request.matricula,
            email=register_request.email,
            curso_id=register_request.curso_id,
            semestre=register_request.semestre,
            password_hash=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        logging.error(f"Erro ao registrar usuário: {e}")
        db.rollback()
        raise
    return new_user

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> model.TokenData:
    return verify_token(token)

def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session) -> model.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = create_access_token(email=user.email, aluno_id=user.aluno_id, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return model.Token(access_token=access_token, token_type="bearer")

