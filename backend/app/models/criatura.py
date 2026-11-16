
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Criatura(Base):
    __tablename__ = "criaturas"

    id: Mapped[int] = mapped_column(primary_key=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"),
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

    pv_maximo: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    classe_armadura: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    observacoes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
