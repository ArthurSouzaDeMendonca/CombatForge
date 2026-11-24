from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CondicaoCombate(Base):
    __tablename__ = "condicoes_combate"

    id: Mapped[int] = mapped_column(primary_key=True)

    participante_id: Mapped[int] = mapped_column(
        ForeignKey(
            "combate_participantes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    duracao_rodadas: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "duracao_rodadas IS NULL OR duracao_rodadas > 0",
            name="ck_condicao_duracao_positiva",
        ),
    )
