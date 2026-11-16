
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash


# Carrega as variáveis de ambiente.
load_dotenv()


# Configura o algoritmo de hash de senhas.
password_hash = PasswordHash.recommended()


# Configurações do JWT.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30


if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY não foi configurada no .env")


def gerar_hash_senha(senha: str) -> str:
    """Transforma uma senha em um hash seguro."""
    return password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se uma senha corresponde ao hash armazenado."""
    return password_hash.verify(senha, senha_hash)


def criar_token_acesso(usuario_id: int) -> str:
    """Gera um token JWT para o usuário autenticado."""

    data_expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EXPIRATION_MINUTES
    )

    dados_token = {
        "sub": str(usuario_id),
        "exp": data_expiracao,
    }

    token = jwt.encode(
        dados_token,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return token