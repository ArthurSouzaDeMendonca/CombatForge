
from pwdlib import PasswordHash


# Configura o algoritmo de hash recomendado pela biblioteca.
password_hash = PasswordHash.recommended()


def gerar_hash_senha(senha: str) -> str:
    """Transforma uma senha em um hash seguro."""
    return password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se uma senha corresponde ao hash armazenado."""
    return password_hash.verify(senha, senha_hash)
