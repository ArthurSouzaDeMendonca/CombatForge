
"""adiciona convite e personagem na campanha

Revision ID: 769374b4d17c
Revises: c088fdcdf6a5
Create Date: 2026-11-17 16:45:22.134494

"""

import secrets
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "769374b4d17c"
down_revision: Union[str, Sequence[str], None] = "c088fdcdf6a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adiciona o personagem à associação da campanha.
    op.add_column(
        "campanha_usuario",
        sa.Column("personagem_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_campanha_usuario_personagem",
        "campanha_usuario",
        "personagens",
        ["personagem_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # Adiciona inicialmente o código como opcional.
    op.add_column(
        "campanhas",
        sa.Column("codigo_convite", sa.String(length=12), nullable=True),
    )

    # Recupera as campanhas já existentes.
    conexao = op.get_bind()

    campanhas = conexao.execute(
        sa.text("SELECT id FROM campanhas")
    ).scalars().all()

    codigos_utilizados = set()

    # Gera um código exclusivo para cada campanha existente.
    for campanha_id in campanhas:
        while True:
            codigo = secrets.token_hex(6).upper()

            if codigo not in codigos_utilizados:
                codigos_utilizados.add(codigo)
                break

        conexao.execute(
            sa.text(
                """
                UPDATE campanhas
                SET codigo_convite = :codigo
                WHERE id = :campanha_id
                """
            ),
            {
                "codigo": codigo,
                "campanha_id": campanha_id,
            },
        )

    # Agora que todas as campanhas possuem código,
    # podemos tornar a coluna obrigatória.
    op.alter_column(
        "campanhas",
        "codigo_convite",
        existing_type=sa.String(length=12),
        nullable=False,
    )

    op.create_unique_constraint(
        "uq_campanhas_codigo_convite",
        "campanhas",
        ["codigo_convite"],
    )

    # Garante que Mestres não tenham personagem associado
    # e que jogadores não possam ficar sem personagem.
    op.create_check_constraint(
        "ck_campanha_usuario_personagem",
        "campanha_usuario",
        """
        (
            papel = 'MESTRE'
            AND personagem_id IS NULL
        )
        OR
        (
            papel = 'JOGADOR'
            AND personagem_id IS NOT NULL
        )
        """,
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_campanha_usuario_personagem",
        "campanha_usuario",
        type_="check",
    )

    op.drop_constraint(
        "uq_campanhas_codigo_convite",
        "campanhas",
        type_="unique",
    )

    op.drop_column("campanhas", "codigo_convite")

    op.drop_constraint(
        "fk_campanha_usuario_personagem",
        "campanha_usuario",
        type_="foreignkey",
    )

    op.drop_column("campanha_usuario", "personagem_id")
