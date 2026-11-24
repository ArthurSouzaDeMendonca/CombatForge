from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CondicaoAplicada(Base):
    __tablename__ = "condicoes_aplicadas"

    id: Mapped[int] = mapped_column(primary_key=True)

    condicao_id: Mapped[int] = mapped_column(
        ForeignKey("condicoes.id", ondelete="RESTRICT"),
        nullable=False,
    )

    personagem_id: Mapped[int | None] = mapped_column(
        ForeignKey("personagens.id", ondelete="CASCADE"),
        nullable=True,
    )

    criatura_id: Mapped[int | None] = mapped_column(
        ForeignKey("criaturas.id", ondelete="CASCADE"),
        nullable=True,
    )

    # Exemplos: "2 rodadas", "1 hora", "até ser removida".
    duracao: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    data_aplicacao: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            """
            (
                personagem_id IS NOT NULL
                AND criatura_id IS NULL
            )
            OR
            (
                personagem_id IS NULL
                AND criatura_id IS NOT NULL
            )
            """,
            name="ck_condicao_aplicada_alvo",
        ),
    )
