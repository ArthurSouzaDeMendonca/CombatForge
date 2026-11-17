
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_usuario_atual
from app.database import get_db
from app.models.personagem import Personagem
from app.models.usuario import Usuario
from app.schemas.personagem_schema import (
    PersonagemCreate,
    PersonagemResponse,
    PersonagemUpdate,
)

router = APIRouter(
    prefix="/personagens",
    tags=["Personagens"],
)


@router.post(
    "/",
    response_model=PersonagemResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_personagem(
    dados: PersonagemCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    personagem = Personagem(
        **dados.model_dump(),
        usuario_id=usuario.id,
    )

    db.add(personagem)
    db.commit()
    db.refresh(personagem)

    return personagem


@router.get(
    "/",
    response_model=list[PersonagemResponse],
)
def listar_personagens(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    personagens = db.scalars(
        select(Personagem)
        .where(Personagem.usuario_id == usuario.id)
        .order_by(Personagem.id)
    ).all()

    return personagens


@router.get(
    "/{personagem_id}",
    response_model=PersonagemResponse,
)
def buscar_personagem(
    personagem_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    personagem = db.scalar(
        select(Personagem).where(
            Personagem.id == personagem_id,
            Personagem.usuario_id == usuario.id,
        )
    )

    if personagem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado.",
        )

    return personagem


@router.put(
    "/{personagem_id}",
    response_model=PersonagemResponse,
)
def atualizar_personagem(
    personagem_id: int,
    dados: PersonagemUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    personagem = db.scalar(
        select(Personagem).where(
            Personagem.id == personagem_id,
            Personagem.usuario_id == usuario.id,
        )
    )

    if personagem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado.",
        )

    for campo, valor in dados.model_dump().items():
        setattr(personagem, campo, valor)

    db.commit()
    db.refresh(personagem)

    return personagem


@router.delete(
    "/{personagem_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_personagem(
    personagem_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    personagem = db.scalar(
        select(Personagem).where(
            Personagem.id == personagem_id,
            Personagem.usuario_id == usuario.id,
        )
    )

    if personagem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado.",
        )

    db.delete(personagem)
    db.commit()
