
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CombateCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)


class CombateResponse(BaseModel):
    id: int
    campanha_id: int
    nome: str
    status: str
    rodada_atual: int
    ordem_turno_atual: int
    data_criacao: datetime
    data_encerramento: datetime | None

    model_config = ConfigDict(from_attributes=True)

class CombatePersonagemAdicionar(BaseModel):
    personagem_id: int = Field(gt=0)
    iniciativa: int


class CombateCriaturaAdicionar(BaseModel):
    criatura_id: int = Field(gt=0)
    iniciativa: int


class CombateParticipanteResponse(BaseModel):
    id: int
    combate_id: int
    personagem_id: int | None
    criatura_id: int | None
    pv_maximo: int
    pv_atual: int
    iniciativa: int
    ordem_turno: int

    model_config = ConfigDict(from_attributes=True)

class CombateParticipanteListResponse(BaseModel):
    id: int
    combate_id: int
    personagem_id: int | None
    criatura_id: int | None
    nome_participante: str
    pv_maximo: int
    pv_atual: int
    iniciativa: int
    ordem_turno: int


class CombateParticipanteUpdate(BaseModel):
    pv_atual: int = Field(ge=0)
    iniciativa: int

class CombateDetalhadoResponse(CombateResponse):
    participantes: list[CombateParticipanteListResponse]