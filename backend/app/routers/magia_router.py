
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_usuario_atual
from app.database import get_db
from app.models.magia import Magia
from app.models.personagem import Personagem
from app.models.usuario import Usuario
from app.schemas.magia_schema import (
    MagiaCreate,
    MagiaResponse,
    MagiaUpdate,
)

router = APIRouter(
    prefix="/personagens/{personagem_id}/magias",
    tags=["Magias"],
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
    response_model=MagiaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_magia(
    personagem_id: int,
    dados: MagiaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    magia = Magia(
        **dados.model_dump(),
        personagem_id=personagem_id,
    )

    db.add(magia)
    db.commit()
    db.refresh(magia)

    return magia


@router.get(
    "/",
    response_model=list[MagiaResponse],
)
def listar_magias(
    personagem_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    magias = db.scalars(
        select(Magia)
        .where(Magia.personagem_id == personagem_id)
        .order_by(Magia.id)
    ).all()

    return magias


@router.get(
    "/{magia_id}",
    response_model=MagiaResponse,
)
def buscar_magia(
    personagem_id: int,
    magia_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    magia = db.scalar(
        select(Magia).where(
            Magia.id == magia_id,
            Magia.personagem_id == personagem_id,
        )
    )

    if magia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Magia não encontrada.",
        )

    return magia


@router.put(
    "/{magia_id}",
    response_model=MagiaResponse,
)
def atualizar_magia(
    personagem_id: int,
    magia_id: int,
    dados: MagiaUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    magia = db.scalar(
        select(Magia).where(
            Magia.id == magia_id,
            Magia.personagem_id == personagem_id,
        )
    )

    if magia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Magia não encontrada.",
        )

    for campo, valor in dados.model_dump().items():
        setattr(magia, campo, valor)

    db.commit()
    db.refresh(magia)

    return magia


@router.delete(
    "/{magia_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_magia(
    personagem_id: int,
    magia_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    magia = db.scalar(
        select(Magia).where(
            Magia.id == magia_id,
            Magia.personagem_id == personagem_id,
        )
    )

    if magia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Magia não encontrada.",
        )

    db.delete(magia)
    db.commit()
