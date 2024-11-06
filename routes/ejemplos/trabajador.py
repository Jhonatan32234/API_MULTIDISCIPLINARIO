# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Trabajador
from schemas import TrabajadorCreate, TrabajadorResponse

router = APIRouter()

@router.get("/", response_model=List[TrabajadorResponse])
def get_trabajador(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trabajador = db.query(Trabajador).offset(skip).limit(limit).all()
    return trabajador

@router.post("/create", response_model=TrabajadorResponse)
def create_trabajador(trabajador: TrabajadorCreate, db: Session = Depends(get_db)):
    new_trabajador = Trabajador(**trabajador.dict())
    db.add(new_trabajador)
    db.commit()
    db.refresh(new_trabajador)
    return new_trabajador

@router.get("/{id_trabajador}", response_model=TrabajadorResponse)
def get_trabajador(id_trabajador: int, db: Session = Depends(get_db)):
    trabajador = db.query(Trabajador).filter(Trabajador.idtrabajador == id_trabajador).first()
    if trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return trabajador

@router.put("/{id_trabajador}", response_model=TrabajadorResponse)
def update_trabajador(id_trabajador: int, trabajador: TrabajadorCreate, db: Session = Depends(get_db)):
    db_trabajador = db.query(Trabajador).filter(Trabajador.idtrabajador == id_trabajador).first()
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    
    for key, value in trabajador.dict().items():
        setattr(db_trabajador, key, value)
    
    db.commit()
    db.refresh(db_trabajador)
    return db_trabajador

@router.delete("/{id_trabajador}", response_model=TrabajadorResponse)
def delete_trabajador(id_trabajador: int, db: Session = Depends(get_db)):
    trabajador = db.query(Trabajador).filter(Trabajador.idtrabajador == id_trabajador).first()
    if trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    
    db.delete(trabajador)
    db.commit()
    return trabajador
