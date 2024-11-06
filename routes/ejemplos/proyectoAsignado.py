# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import ProyectoAsignado
from schemas import ProyectoAsignadoCreate, ProyectoAsignadoResponse

router = APIRouter()

@router.get("/", response_model=List[ProyectoAsignadoResponse])
def get_proyectoAsignado(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proyectoAsignado = db.query(ProyectoAsignado).offset(skip).limit(limit).all()
    return proyectoAsignado

@router.post("/create", response_model=ProyectoAsignadoResponse)
def create_proyectoAsignado(proyectoAsignado: ProyectoAsignadoCreate, db: Session = Depends(get_db)):
    new_proyectoAsignado = ProyectoAsignado(**proyectoAsignado.dict())
    db.add(new_proyectoAsignado)
    db.commit()
    db.refresh(new_proyectoAsignado)
    return new_proyectoAsignado

@router.get("/{id_proyectoAsignado}", response_model=ProyectoAsignadoResponse)
def get_proyectoAsignado(id_proyectoAsignado: int, db: Session = Depends(get_db)):
    proyectoAsignado = db.query(ProyectoAsignadoResponse).filter(ProyectoAsignado.idproyectoasignado == id_proyectoAsignado).first()
    if proyectoAsignado is None:
        raise HTTPException(status_code=404, detail="Proyecto Asignado no encontrado")
    return proyectoAsignado

@router.put("/{id_proyectoAisgnado}", response_model=ProyectoAsignadoResponse)
def update_proyectoAsignado(id_proyectoAsignado: int, proyectoAsignado: ProyectoAsignadoCreate, db: Session = Depends(get_db)):
    db_proyectoAsignado = db.query(ProyectoAsignado).filter(ProyectoAsignado.idproyectoasignado == id_proyectoAsignado).first()
    if db_proyectoAsignado is None:
        raise HTTPException(status_code=404, detail="Proyecto Asignado no encontrado")
    
    for key, value in proyectoAsignado.dict().items():
        setattr(db_proyectoAsignado, key, value)
    
    db.commit()
    db.refresh(db_proyectoAsignado)
    return db_proyectoAsignado

@router.delete("/{id_proyectoAsignado}", response_model=ProyectoAsignadoResponse)
def delete_proyectoAsignado(id_proyectoAsignado: int, db: Session = Depends(get_db)):
    proyectoAsignado = db.query(ProyectoAsignado).filter(ProyectoAsignado.idproyectoasignado == id_proyectoAsignado).first()
    if proyectoAsignado is None:
        raise HTTPException(status_code=404, detail="Proyecto Asignado no encontrado")
    
    db.delete(proyectoAsignado)
    db.commit()
    return proyectoAsignado
