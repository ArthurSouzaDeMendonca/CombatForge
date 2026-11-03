
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Habilidade(Base):
    __tablename__ = "habilidades"

    id: Mapped[int] = mapped_column(primary_key=True)

    personagem_id: Mapped[int] = mapped_column(
        ForeignKey("personagens.id", ondelete="CASCADE"),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    usos_maximos: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    usos_atuais: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    duracao: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
