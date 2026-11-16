
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Combate(Base):
    __tablename__ = "combates"

    id: Mapped[int] = mapped_column(primary_key=True)

    campanha_id: Mapped[int] = mapped_column(
        ForeignKey("campanhas.id", ondelete="CASCADE"),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ATIVO",
        nullable=False,
    )

    rodada_atual: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    ordem_turno_atual: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    data_encerramento: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
