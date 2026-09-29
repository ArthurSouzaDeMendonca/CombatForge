from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CampanhaUsuario(Base):
    __tablename__ = "campanha_usuario"

    campanha_id: Mapped[int] = mapped_column(
        ForeignKey("campanhas.id", ondelete="CASCADE"),
        primary_key=True,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        primary_key=True,
    )

    papel: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "papel IN ('MESTRE', 'JOGADOR')",
            name="ck_campanha_usuario_papel",
        ),
        Index(
            "uq_campanha_usuario_mestre",
            "campanha_id",
            unique=True,
            postgresql_where=text("papel = 'MESTRE'"),
        ),
    )