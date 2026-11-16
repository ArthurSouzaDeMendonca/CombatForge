
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers import usuario_router, autenticacao_router


app = FastAPI(
    title="CombatForge API",
    description="API do sistema CombatForge.",
    version="1.0.0",
)


# Registra as rotas de usuários.
app.include_router(usuario_router.router)
app.include_router(autenticacao_router.router)


@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "CombatForge API funcionando!"}
