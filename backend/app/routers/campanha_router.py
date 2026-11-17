import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.auth import get_usuario_atual
from app.database import get_db
from app.models.campanha import Campanha
from app.models.campanha_usuario import CampanhaUsuario
from app.models.usuario import Usuario
from app.schemas.campanha_schema import CampanhaCreate, CampanhaResponse, CampanhaUpdate, CampanhaEntrar
from app.models.personagem import Personagem


def gerar_codigo_convite() -> str:
    return secrets.token_hex(6).upper()

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
    for tentativa in range(5):
        campanha = Campanha(
            nome=dados.nome,
            descricao=dados.descricao,
            codigo_convite=gerar_codigo_convite(),
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
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Não foi possível gerar um código de convite exclusivo.",
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

@router.post(
    "/entrar",
    response_model=CampanhaResponse,
)
def entrar_em_campanha(
    dados: CampanhaEntrar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    # Procura a campanha pelo código de convite.
    campanha = db.scalar(
        select(Campanha).where(
            Campanha.codigo_convite == dados.codigo_convite.strip().upper()
        )
    )

    if campanha is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Código de convite inválido.",
        )

    # Verifica se o usuário já participa da campanha.
    associacao_existente = db.scalar(
        select(CampanhaUsuario).where(
            CampanhaUsuario.campanha_id == campanha.id,
            CampanhaUsuario.usuario_id == usuario.id,
        )
    )

    if associacao_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Você já participa desta campanha.",
        )

    # Verifica se o personagem pertence ao usuário.
    personagem = db.scalar(
        select(Personagem).where(
            Personagem.id == dados.personagem_id,
            Personagem.usuario_id == usuario.id,
        )
    )

    if personagem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personagem não encontrado.",
        )

    # Registra o usuário como jogador da campanha.
    associacao = CampanhaUsuario(
        campanha_id=campanha.id,
        usuario_id=usuario.id,
        papel="JOGADOR",
        personagem_id=personagem.id,
    )

    try:
        db.add(associacao)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível entrar na campanha.",
        )

    return campanha