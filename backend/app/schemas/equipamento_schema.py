
from pydantic import BaseModel, ConfigDict, Field


class EquipamentoBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    tipo: str = Field(min_length=1, max_length=50)
    descricao: str | None = None

    bonus_ataque: int | None = None
    bonus_dano: int | None = None
    bonus_ca: int | None = None

    equipado: bool = False


class EquipamentoCreate(EquipamentoBase):
    pass


class EquipamentoUpdate(EquipamentoBase):
    pass


class EquipamentoResponse(EquipamentoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
