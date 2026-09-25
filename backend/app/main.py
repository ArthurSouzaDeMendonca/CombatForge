from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import get_db


app = FastAPI()


@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "CombatForge API funcionando!"}

