
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_usuario_atual
from app.database import get_db
from app.models.equipamento import Equipamento
from app.models.personagem import Personagem
from app.models.usuario import Usuario
from app.schemas.equipamento_schema import (
    EquipamentoCreate,
    EquipamentoResponse,
    EquipamentoUpdate,
)

router = APIRouter(
    prefix="/personagens/{personagem_id}/equipamentos",
    tags=["Equipamentos"],
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
    response_model=EquipamentoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_equipamento(
    personagem_id: int,
    dados: EquipamentoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    equipamento = Equipamento(
        **dados.model_dump(),
        personagem_id=personagem_id,
    )

    db.add(equipamento)
    db.commit()
    db.refresh(equipamento)

    return equipamento


@router.get(
    "/",
    response_model=list[EquipamentoResponse],
)
def listar_equipamentos(
    personagem_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    equipamentos = db.scalars(
        select(Equipamento)
        .where(Equipamento.personagem_id == personagem_id)
        .order_by(Equipamento.id)
    ).all()

    return equipamentos


@router.get(
    "/{equipamento_id}",
    response_model=EquipamentoResponse,
)
def buscar_equipamento(
    personagem_id: int,
    equipamento_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    equipamento = db.scalar(
        select(Equipamento).where(
            Equipamento.id == equipamento_id,
            Equipamento.personagem_id == personagem_id,
        )
    )

    if equipamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipamento não encontrado.",
        )

    return equipamento


@router.put(
    "/{equipamento_id}",
    response_model=EquipamentoResponse,
)
def atualizar_equipamento(
    personagem_id: int,
    equipamento_id: int,
    dados: EquipamentoUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    equipamento = db.scalar(
        select(Equipamento).where(
            Equipamento.id == equipamento_id,
            Equipamento.personagem_id == personagem_id,
        )
    )

    if equipamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipamento não encontrado.",
        )

    for campo, valor in dados.model_dump().items():
        setattr(equipamento, campo, valor)

    db.commit()
    db.refresh(equipamento)

    return equipamento


@router.delete(
    "/{equipamento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_equipamento(
    personagem_id: int,
    equipamento_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    buscar_personagem_do_usuario(
        personagem_id,
        usuario.id,
        db,
    )

    equipamento = db.scalar(
        select(Equipamento).where(
            Equipamento.id == equipamento_id,
            Equipamento.personagem_id == personagem_id,
        )
    )

    if equipamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipamento não encontrado.",
        )

    db.delete(equipamento)
    db.commit()
