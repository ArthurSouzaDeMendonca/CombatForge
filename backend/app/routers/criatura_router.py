
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_usuario_atual
from app.database import get_db
from app.models.criatura import Criatura
from app.models.usuario import Usuario
from app.schemas.criatura_schema import (
    CriaturaCreate,
    CriaturaResponse,
    CriaturaUpdate,
)

router = APIRouter(
    prefix="/criaturas",
    tags=["Criaturas"],
)


@router.post(
    "/",
    response_model=CriaturaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_criatura(
    dados: CriaturaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    criatura = Criatura(
        **dados.model_dump(),
        usuario_id=usuario.id,
    )

    db.add(criatura)
    db.commit()
    db.refresh(criatura)

    return criatura


@router.get(
    "/",
    response_model=list[CriaturaResponse],
)
def listar_criaturas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    criaturas = db.scalars(
        select(Criatura)
        .where(Criatura.usuario_id == usuario.id)
        .order_by(Criatura.id)
    ).all()

    return criaturas


@router.get(
    "/{criatura_id}",
    response_model=CriaturaResponse,
)
def buscar_criatura(
    criatura_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    criatura = db.scalar(
        select(Criatura).where(
            Criatura.id == criatura_id,
            Criatura.usuario_id == usuario.id,
        )
    )

    if criatura is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criatura não encontrada.",
        )

    return criatura


@router.put(
    "/{criatura_id}",
    response_model=CriaturaResponse,
)
def atualizar_criatura(
    criatura_id: int,
    dados: CriaturaUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    criatura = db.scalar(
        select(Criatura).where(
            Criatura.id == criatura_id,
            Criatura.usuario_id == usuario.id,
        )
    )

    if criatura is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criatura não encontrada.",
        )

    for campo, valor in dados.model_dump().items():
        setattr(criatura, campo, valor)

    db.commit()
    db.refresh(criatura)

    return criatura


@router.delete(
    "/{criatura_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_criatura(
    criatura_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    criatura = db.scalar(
        select(Criatura).where(
            Criatura.id == criatura_id,
            Criatura.usuario_id == usuario.id,
        )
    )

    if criatura is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criatura não encontrada.",
        )

    db.delete(criatura)
    db.commit()
