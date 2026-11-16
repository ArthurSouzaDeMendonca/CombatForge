
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CombateParticipante(Base):
    __tablename__ = "combate_participantes"

    id: Mapped[int] = mapped_column(primary_key=True)

    combate_id: Mapped[int] = mapped_column(
        ForeignKey("combates.id", ondelete="CASCADE"),
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

    pv_maximo: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    pv_atual: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    iniciativa: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    ordem_turno: Mapped[int] = mapped_column(
        Integer,
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
            name="ck_combate_participante_tipo",
        ),
        UniqueConstraint(
            "combate_id",
            "personagem_id",
            name="uq_combate_personagem",
        ),
        UniqueConstraint(
            "combate_id",
            "criatura_id",
            name="uq_combate_criatura",
        ),
        UniqueConstraint(
            "combate_id",
            "ordem_turno",
            name="uq_combate_ordem_turno",
        ),
    )
