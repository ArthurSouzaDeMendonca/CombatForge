
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.autenticacao_schema import LoginRequest, TokenResponse
from app.security import verificar_senha, criar_token_acesso


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db),
):
    # Normaliza o e-mail recebido.
    email = str(dados.email).lower()

    # Procura o usuário no banco de dados.
    usuario = db.scalar(
        select(Usuario).where(Usuario.email == email)
    )

    # Verifica se o usuário existe e se a senha está correta.
    if not usuario or not verificar_senha(
        dados.senha,
        usuario.senha_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera o token de acesso.
    token = criar_token_acesso(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
