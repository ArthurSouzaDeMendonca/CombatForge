
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Personagem(Base):
    __tablename__ = "personagens"

    id: Mapped[int] = mapped_column(primary_key=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    raca: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    classe: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    nivel: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    forca: Mapped[int] = mapped_column(Integer, nullable=False)
    destreza: Mapped[int] = mapped_column(Integer, nullable=False)
    constituicao: Mapped[int] = mapped_column(Integer, nullable=False)
    inteligencia: Mapped[int] = mapped_column(Integer, nullable=False)
    sabedoria: Mapped[int] = mapped_column(Integer, nullable=False)
    carisma: Mapped[int] = mapped_column(Integer, nullable=False)

    pv_maximo: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    pv_atual: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
