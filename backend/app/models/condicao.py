
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Condicao(Base):
    __tablename__ = "condicoes"

    id: Mapped[int] = mapped_column(primary_key=True)

    # NULL representa uma condição oficial do sistema.
    # Um ID representa uma condição personalizada de um usuário.
    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=True,
    )

    nome: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    descricao: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "usuario_id",
            "nome",
            name="uq_condicao_usuario_nome",
        ),
    )
