from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import get_usuario_atual
from app.database import get_db
from app.models.campanha import Campanha
from app.models.campanha_usuario import CampanhaUsuario
from app.models.usuario import Usuario
from app.schemas.campanha_schema import CampanhaCreate, CampanhaResponse, CampanhaUpdate


router = APIRouter(
    prefix="/campanhas",
    tags=["Campanhas"],
)


@router.post(
    "/",
    response_model=CampanhaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_campanha(
    dados: CampanhaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    campanha = Campanha(
        nome=dados.nome,
        descricao=dados.descricao,
    )

    try:
        db.add(campanha)
        db.flush()

        associacao = CampanhaUsuario(
            campanha_id=campanha.id,
            usuario_id=usuario.id,
            papel="MESTRE",
        )

        db.add(associacao)
        db.commit()
        db.refresh(campanha)

        return campanha

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível criar a campanha.",
        )


@router.get(
    "/",
    response_model=list[CampanhaResponse],
)
def listar_campanhas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    consulta = (
        select(Campanha)
        .join(
            CampanhaUsuario,
            CampanhaUsuario.campanha_id == Campanha.id,
        )
        .where(CampanhaUsuario.usuario_id == usuario.id)
        .order_by(Campanha.data_criacao.desc())
    )

    campanhas = db.scalars(consulta).all()

    return campanhas


@router.put(
    "/{campanha_id}",
    response_model=CampanhaResponse,
)
def atualizar_campanha(
    campanha_id: int,
    dados: CampanhaUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    consulta = (
        select(CampanhaUsuario)
        .where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    associacao = db.scalar(consulta)

    if associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campanha não encontrada.",
        )

    if associacao.papel != "MESTRE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o Mestre pode editar a campanha.",
        )

    campanha = db.get(Campanha, campanha_id)

    campanha.nome = dados.nome
    campanha.descricao = dados.descricao

    db.commit()
    db.refresh(campanha)

    return campanha



@router.delete(
    "/{campanha_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_campanha(
    campanha_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    consulta = (
        select(CampanhaUsuario)
        .where(
            CampanhaUsuario.campanha_id == campanha_id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    associacao = db.scalar(consulta)

    if associacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campanha não encontrada.",
        )

    if associacao.papel != "MESTRE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o Mestre pode excluir a campanha.",
        )

    campanha = db.get(Campanha, campanha_id)

    db.delete(campanha)
    db.commit()

