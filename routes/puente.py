# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Puente
from schemas import puenteCreate, puenteResponse

router = APIRouter()


@router.get("/", response_model=List[puenteResponse])
def get_puente(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    puente = db.query(Puente).offset(skip).limit(limit).all()
    return puente

@router.post("/create", response_model=puenteResponse)
def create_puente(puente: puenteCreate, db: Session = Depends(get_db)):
    new_puente = Puente(**puente.dict())
    db.add(new_puente)
    db.commit()
    db.refresh(new_puente)
    return new_puente

@router.get("/{id_puente}", response_model=puenteResponse)
def get_puente(id_puente: int, db: Session = Depends(get_db)):
    puente = db.query(Puente).filter(Puente.idpuente == id_puente).first()
    if puente is None:
        raise HTTPException(status_code=404, detail="Puente no encontrado")
    return puente

@router.put("/{id_puente}", response_model=puenteResponse)
def update_puente(id_puente: int, puente: puenteCreate, db: Session = Depends(get_db)):
    db_puente = db.query(Puente).filter(Puente.idpuente == id_puente).first()
    if db_puente is None:
        raise HTTPException(status_code=404, detail="Puente no encontrado")
    
    for key, value in puente.dict().items():
        setattr(db_puente, key, value)
    
    db.commit()
    db.refresh(db_puente)
    return db_puente

@router.delete("/{id_puente}", response_model=puenteResponse)
def delete_puente(id_puente: int, db: Session = Depends(get_db)):
    puente = db.query(Puente).filter(Puente.idpuente == id_puente).first()
    if puente is None:
        raise HTTPException(status_code=404, detail="Puente no encontrado")
    
    db.delete(puente)
    db.commit()
    return puente
