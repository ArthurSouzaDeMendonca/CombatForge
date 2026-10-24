
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Magia(Base):
    __tablename__ = "magias"

    id: Mapped[int] = mapped_column(primary_key=True)

    personagem_id: Mapped[int] = mapped_column(
        ForeignKey("personagens.id", ondelete="CASCADE"),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    nivel: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    formula_dano: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    formula_cura: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    tipo_dano: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    alcance: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    duracao: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    componentes: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    concentracao: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
