
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# Dados necessários para cadastrar um usuário.
class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)

# Dados que a API poderá devolver ao consultar um usuário.
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)