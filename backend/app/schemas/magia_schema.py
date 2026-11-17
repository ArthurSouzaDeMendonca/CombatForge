
from pydantic import BaseModel, ConfigDict, Field


class MagiaBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    nivel: int = Field(ge=0, le=9)
    descricao: str | None = None
    formula_dano: str | None = Field(default=None, max_length=50)
    formula_cura: str | None = Field(default=None, max_length=50)
    tipo_dano: str | None = Field(default=None, max_length=30)
    alcance: str | None = Field(default=None, max_length=100)
    duracao: str | None = Field(default=None, max_length=100)
    componentes: str | None = Field(default=None, max_length=50)
    concentracao: bool = False


class MagiaCreate(MagiaBase):
    pass


class MagiaUpdate(MagiaBase):
    pass


class MagiaResponse(MagiaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
