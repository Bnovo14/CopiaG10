from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)

class AuthenticationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail="Usuário ou senha inválidos")

class InvalidTokenException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)