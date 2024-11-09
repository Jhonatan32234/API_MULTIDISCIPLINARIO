# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Nivel
from schemas import nivelCreate, nivelResponse

router = APIRouter()


@router.get("/", response_model=List[nivelResponse])
def get_nivel(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    nivel = db.query(Nivel).offset(skip).limit(limit).all()
    return nivel

@router.post("/create", response_model=nivelResponse)
def create_nivel(nivel: nivelCreate, db: Session = Depends(get_db)):
    new_nivel = Nivel(**nivel.dict())
    db.add(new_nivel)
    db.commit()
    db.refresh(new_nivel)
    return new_nivel

@router.get("/{id_nivel}", response_model=nivelResponse)
def get_nivel(id_nivel: int, db: Session = Depends(get_db)):
    nivel = db.query(Nivel).filter(Nivel.idnivel == id_nivel).first()
    if nivel is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return nivel

@router.put("/{id_nivel}", response_model=nivelResponse)
def update_nivel(id_nivel: int, nivel: nivelCreate, db: Session = Depends(get_db)):
    db_nivel = db.query(Nivel).filter(Nivel.idnivel == id_nivel).first()
    if db_nivel is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    
    for key, value in nivel.dict().items():
        setattr(db_nivel, key, value)
    
    db.commit()
    db.refresh(db_nivel)
    return db_nivel

@router.delete("/{id_nivel}", response_model=nivelResponse)
def delete_nivel(id_nivel: int, db: Session = Depends(get_db)):
    nivel = db.query(Nivel).filter(Nivel.idnivel == id_nivel).first()
    if nivel is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    
    db.delete(nivel)
    db.commit()
    return nivel
