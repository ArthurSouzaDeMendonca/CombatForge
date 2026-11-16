
from pydantic import BaseModel, EmailStr, Field


# Dados enviados pelo usuário durante o login.
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1)


# Dados devolvidos após um login bem-sucedido.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
