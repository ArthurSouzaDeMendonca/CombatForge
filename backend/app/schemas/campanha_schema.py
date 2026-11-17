from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CampanhaCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    descricao: str | None = None


class CampanhaResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    data_criacao: datetime
    codigo_convite: str

    model_config = ConfigDict(from_attributes=True)

class CampanhaUpdate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    descricao: str | None = None

class CampanhaEntrar(BaseModel):
    codigo_convite: str = Field(min_length=12, max_length=12)
    personagem_id: int = Field(gt=0)