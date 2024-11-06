# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Materia
from schemas import MateriaCreate, MateriaResponse

router = APIRouter()

@router.get("/", response_model=List[MateriaResponse])
def get_materias(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    materias = db.query(Materia).offset(skip).limit(limit).all()
    return materias

@router.post("/", response_model=MateriaResponse)
def create_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    new_materia = Materia(**materia.dict())
    db.add(new_materia)
    db.commit()
    db.refresh(new_materia)
    return new_materia

@router.get("/{id_materia}", response_model=MateriaResponse)
def get_materia(id_materia: int, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id_materia == id_materia).first()
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia

@router.put("/{id_materia}", response_model=MateriaResponse)
def update_materia(id_materia: int, materia: MateriaCreate, db: Session = Depends(get_db)):
    db_materia = db.query(Materia).filter(Materia.id_materia == id_materia).first()
    if db_materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    
    for key, value in materia.dict().items():
        setattr(db_materia, key, value)
    
    db.commit()
    db.refresh(db_materia)
    return db_materia

@router.delete("/{id_materia}", response_model=MateriaResponse)
def delete_materia(id_materia: int, db: Session = Depends(get_db)):
    materia = db.query(Materia).filter(Materia.id_materia == id_materia).first()
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    
    db.delete(materia)
    db.commit()
    return materia
