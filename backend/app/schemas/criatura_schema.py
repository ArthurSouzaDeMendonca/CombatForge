
from pydantic import BaseModel, ConfigDict, Field


class CriaturaBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str | None = None
    pv_maximo: int = Field(ge=1)
    classe_armadura: int = Field(ge=0)
    observacoes: str | None = None


class CriaturaCreate(CriaturaBase):
    pass


class CriaturaUpdate(CriaturaBase):
    pass


class CriaturaResponse(CriaturaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
