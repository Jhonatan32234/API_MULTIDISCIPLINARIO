# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Pared
from schemas import paredCreate, paredResponse

router = APIRouter()


@router.get("/", response_model=List[paredResponse])
def get_pared(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pared = db.query(Pared).offset(skip).limit(limit).all()
    return pared

@router.post("/create", response_model=paredResponse)
def create_pared(pared: paredCreate, db: Session = Depends(get_db)):
    new_pared = Pared(**pared.dict())
    db.add(new_pared)
    db.commit()
    db.refresh(new_pared)
    return new_pared

@router.get("/{id_pared}", response_model=paredResponse)
def get_pared(id_pared: int, db: Session = Depends(get_db)):
    pared = db.query(Pared).filter(Pared.idpared == id_pared).first()
    if pared is None:
        raise HTTPException(status_code=404, detail="Pared no encontrado")
    return pared

@router.put("/{id_pared}", response_model=paredResponse)
def update_pared(id_pared: int, pared: paredCreate, db: Session = Depends(get_db)):
    db_pared = db.query(Pared).filter(Pared.idpared == id_pared).first()
    if db_pared is None:
        raise HTTPException(status_code=404, detail="Pared no encontrado")
    
    for key, value in pared.dict().items():
        setattr(db_pared, key, value)
    
    db.commit()
    db.refresh(db_pared)
    return db_pared

@router.delete("/{id_pared}", response_model=paredResponse)
def delete_pared(id_pared: int, db: Session = Depends(get_db)):
    pared = db.query(Pared).filter(Pared.idpared == id_pared).first()
    if pared is None:
        raise HTTPException(status_code=404, detail="Pared no encontrado")
    
    db.delete(pared)
    db.commit()
    return pared
