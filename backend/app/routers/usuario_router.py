
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.security import gerar_hash_senha
from app.auth import get_usuario_atual

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
)

@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_usuario(
    dados: UsuarioCreate,
    db: Session = Depends(get_db),
):
    # Normaliza o e-mail para evitar cadastros com diferenças de maiúsculas.
    email = str(dados.email).lower()

    # Verifica se já existe um usuário com esse e-mail.
    usuario_existente = db.scalar(
        select(Usuario).where(Usuario.email == email)
    )

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este e-mail já está cadastrado.",
        )

    # Cria o usuário utilizando o hash da senha.
    novo_usuario = Usuario(
        nome=dados.nome,
        email=email,
        senha_hash=gerar_hash_senha(dados.senha),
    )

    db.add(novo_usuario)

    try:
        db.commit()
        db.refresh(novo_usuario)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível cadastrar. Verifique se o e-mail já existe.",
        )

    return novo_usuario


@router.get(
    "/me",
    response_model=UsuarioResponse,
)
def obter_usuario_atual(
    usuario: Usuario = Depends(get_usuario_atual),
):
    """Retorna os dados do usuário autenticado."""

    return usuario
