
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PersonagemBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    raca: str = Field(min_length=1, max_length=50)
    classe: str = Field(min_length=1, max_length=50)

    nivel: int = Field(default=1, ge=1, le=20)

    forca: int = Field(ge=1, le=30)
    destreza: int = Field(ge=1, le=30)
    constituicao: int = Field(ge=1, le=30)
    inteligencia: int = Field(ge=1, le=30)
    sabedoria: int = Field(ge=1, le=30)
    carisma: int = Field(ge=1, le=30)

    pv_maximo: int = Field(ge=1)
    pv_atual: int = Field(ge=0)

    @model_validator(mode="after")
    def validar_pontos_de_vida(self):
        if self.pv_atual > self.pv_maximo:
            raise ValueError(
                "Os pontos de vida atuais não podem superar os pontos de vida máximos."
            )

        return self


class PersonagemCreate(PersonagemBase):
    pass


class PersonagemUpdate(PersonagemBase):
    pass


class PersonagemResponse(PersonagemBase):
    id: int
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)
