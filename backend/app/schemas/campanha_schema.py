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

    model_config = ConfigDict(from_attributes=True)

class CampanhaUpdate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    descricao: str | None = None