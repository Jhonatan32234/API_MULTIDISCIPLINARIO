# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import terminalCodigo
from schemas import terminalCodigoCreate, terminalCodigoResponse

router = APIRouter()


@router.get("/", response_model=List[terminalCodigoResponse])
def get_terminalcodigo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terminalcodigo = db.query(terminalCodigo).offset(skip).limit(limit).all()
    return terminalcodigo

@router.post("/create", response_model=terminalCodigoResponse)
def create_terminalcodigo(terminalcodigo: terminalCodigoCreate, db: Session = Depends(get_db)):
    new_terminalcodigo = terminalCodigo(**terminalcodigo.dict())
    db.add(new_terminalcodigo)
    db.commit()
    db.refresh(new_terminalcodigo)
    return new_terminalcodigo

@router.get("/{id_terminalcodigo}", response_model=terminalCodigoResponse)
def get_terminalcodigo(id_terminalcodigo: int, db: Session = Depends(get_db)):
    terminalcodigo = db.query(terminalCodigo).filter(terminalCodigo.idterminalcodigo == id_terminalcodigo).first()
    if terminalcodigo is None:
        raise HTTPException(status_code=404, detail="bloqueCodigo no encontrado")
    return terminalcodigo

@router.put("/{id_terminalcodigo}", response_model=terminalCodigoResponse)
def update_terminalcodigo(id_terminalcodigo: int, terminalcodigo: terminalCodigoCreate, db: Session = Depends(get_db)):
    db_terminalcodigo = db.query(terminalCodigo).filter(terminalCodigo.idterminalcodigo == id_terminalcodigo).first()
    if db_terminalcodigo is None:
        raise HTTPException(status_code=404, detail="terminalCodigo no encontrado")
    
    for key, value in terminalcodigo.dict().items():
        setattr(db_terminalcodigo, key, value)
    
    db.commit()
    db.refresh(db_terminalcodigo)
    return db_terminalcodigo

@router.delete("/{id_terminalcodigo}", response_model=terminalCodigoResponse)
def delete_terminalcodigo(id_terminalcodigo: int, db: Session = Depends(get_db)):
    terminalcodigo = db.query(terminalCodigo).filter(terminalCodigo.idterminalcodigo == id_terminalcodigo).first()
    if terminalcodigo is None:
        raise HTTPException(status_code=404, detail="terminalCodigo no encontrado")
    db.delete(terminalcodigo)
    db.commit()
    return terminalcodigo
