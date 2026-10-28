
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Equipamento(Base):
    __tablename__ = "equipamentos"

    id: Mapped[int] = mapped_column(primary_key=True)

    personagem_id: Mapped[int] = mapped_column(
        ForeignKey("personagens.id", ondelete="CASCADE"),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    bonus_ataque: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    bonus_dano: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    bonus_ca: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    equipado: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
