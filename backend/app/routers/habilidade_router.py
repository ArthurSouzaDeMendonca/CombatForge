
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_usuario_atual
from app.database import get_db
from app.models.habilidade import Habilidade
from app.models.personagem import Personagem
from app.models.usuario import Usuario
from app.schemas.habilidade_schema import (
    HabilidadeCreate,
    HabilidadeResponse,
    HabilidadeUpdate,
)

router = APIRouter(
    prefix="/personagens/{personagem_id}/habilidades",
    tags=["Habilidades"],
)


def buscar_personagem_do_usuario(
    personagem_id: int,
    usuario_id: int,
    db: Session,
) -> Personagem:
    personagem = db.scalar(
        select(Personagem).where(
            Personagem.id == personagem_id,
            Personagem.usuario_id == usuario_id,
        )
    )

    if personagem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado.",
        )

    return personagem


@router.post(
    "/",
    response_model=HabilidadeResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_habilidade(
    personagem_id: int,
    dados: HabilidadeCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    habilidade = Habilidade(
        **dados.model_dump(),
        personagem_id=personagem_id,
    )

    db.add(habilidade)
    db.commit()
    db.refresh(habilidade)

    return habilidade


@router.get(
    "/",
    response_model=list[HabilidadeResponse],
)
def listar_habilidades(
    personagem_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    habilidades = db.scalars(
        select(Habilidade)
        .where(Habilidade.personagem_id == personagem_id)
        .order_by(Habilidade.id)
    ).all()

    return habilidades


@router.get(
    "/{habilidade_id}",
    response_model=HabilidadeResponse,
)
def buscar_habilidade(
    personagem_id: int,
    habilidade_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    habilidade = db.scalar(
        select(Habilidade).where(
            Habilidade.id == habilidade_id,
            Habilidade.personagem_id == personagem_id,
        )
    )

    if habilidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habilidade não encontrada.",
        )

    return habilidade


@router.put(
    "/{habilidade_id}",
    response_model=HabilidadeResponse,
)
def atualizar_habilidade(
    personagem_id: int,
    habilidade_id: int,
    dados: HabilidadeUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    habilidade = db.scalar(
        select(Habilidade).where(
            Habilidade.id == habilidade_id,
            Habilidade.personagem_id == personagem_id,
        )
    )

    if habilidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habilidade não encontrada.",
        )

    for campo, valor in dados.model_dump().items():
        setattr(habilidade, campo, valor)

    db.commit()
    db.refresh(habilidade)

    return habilidade


@router.delete(
    "/{habilidade_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_habilidade(
    personagem_id: int,
    habilidade_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    habilidade = db.scalar(
        select(Habilidade).where(
            Habilidade.id == habilidade_id,
            Habilidade.personagem_id == personagem_id,
        )
    )

    if habilidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habilidade não encontrada.",
        )

    db.delete(habilidade)
    db.commit()
