from uuid import UUID
from pydantic import BaseModel, EmailStr

class RegisterPersonRequest(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    password: str
    confirm_password: str
    #adicionar quando revisar os pré-requisitos. Montar um MER futuramente!

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    person_id: UUID
    email: EmailStr

    def get_uuid(self) -> UUID | None:
        if self.person_id:
            return self.person_id
        return None