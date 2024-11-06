# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import JefeProyecto
from schemas import JefeProyectoCreate, JefeProyectoResponse

router = APIRouter()

@router.get("/", response_model=List[JefeProyectoResponse])
def get_jefe(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jefe = db.query(JefeProyecto).offset(skip).limit(limit).all()
    return jefe

@router.post("/create", response_model=JefeProyectoResponse)
def create_jefe(jefe: JefeProyectoCreate, db: Session = Depends(get_db)):
    new_jefe = JefeProyecto(**jefe.dict())
    db.add(new_jefe)
    db.commit()
    db.refresh(new_jefe)
    return new_jefe

@router.get("/{id_jefe}", response_model=JefeProyectoResponse)
def get_jefe(id_jefe: int, db: Session = Depends(get_db)):
    jefe = db.query(JefeProyecto).filter(JefeProyecto.idjefeproyecto == id_jefe).first()
    if jefe is None:
        raise HTTPException(status_code=404, detail="Jefe no encontrado")
    return jefe

@router.put("/{id_jefe}", response_model=JefeProyectoResponse)
def update_jefe(id_jefe: int, jefe: JefeProyectoCreate, db: Session = Depends(get_db)):
    db_jefe = db.query(JefeProyecto).filter(JefeProyecto.idjefeproyecto == id_jefe).first()
    if db_jefe is None:
        raise HTTPException(status_code=404, detail="Jefe no encontrado")
    
    for key, value in jefe.dict().items():
        setattr(db_jefe, key, value)
    
    db.commit()
    db.refresh(db_jefe)
    return db_jefe

@router.delete("/{id_jefe}", response_model=JefeProyectoResponse)
def delete_jefe(id_jefe: int, db: Session = Depends(get_db)):
    jefe = db.query(JefeProyecto).filter(JefeProyecto.idjefeproyecto == id_jefe).first()
    if jefe is None:
        raise HTTPException(status_code=404, detail="Jefe no encontrado")
    
    db.delete(jefe)
    db.commit()
    return jefe
