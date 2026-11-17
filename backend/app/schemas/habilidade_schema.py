
from pydantic import BaseModel, ConfigDict, Field


class HabilidadeBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str | None = None
    usos_maximos: int | None = Field(default=None, ge=0)
    usos_atuais: int | None = Field(default=None, ge=0)
    duracao: str | None = Field(default=None, max_length=100)


class HabilidadeCreate(HabilidadeBase):
    pass


class HabilidadeUpdate(HabilidadeBase):
    pass


class HabilidadeResponse(HabilidadeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
