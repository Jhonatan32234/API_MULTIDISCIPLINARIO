# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Proyecto
from schemas import ProyectoCreate, ProyectoResponse

router = APIRouter()

@router.get("/", response_model=List[ProyectoResponse])
def get_proyecto(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proyecto = db.query(Proyecto).offset(skip).limit(limit).all()
    return proyecto

@router.post("/create", response_model=ProyectoResponse)
def create_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    new_proyecto = Proyecto(**proyecto.dict())
    db.add(new_proyecto)
    db.commit()
    db.refresh(new_proyecto)
    return new_proyecto

@router.get("/{id_proyecto}", response_model=ProyectoResponse)
def get_proyecto(id_proyecto: int, db: Session = Depends(get_db)):
    proyecto = db.query(Proyecto).filter(Proyecto.idProyecto == id_proyecto).first()
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto

@router.put("/{id_proyecto}", response_model=ProyectoResponse)
def update_proyecto(id_proyecto: int, proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = db.query(Proyecto).filter(Proyecto.idProyecto == id_proyecto).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    for key, value in proyecto.dict().items():
        setattr(db_proyecto, key, value)
    
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.delete("/{id_proyecto}", response_model=ProyectoResponse)
def delete_proyecto(id_proyecto: int, db: Session = Depends(get_db)):
    proyecto = db.query(Proyecto).filter(Proyecto.idProyecto == id_proyecto).first()
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    db.delete(proyecto)
    db.commit()
    return proyecto
