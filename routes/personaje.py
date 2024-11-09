# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Personaje
from schemas import personajeCreate, personajeResponse

router = APIRouter()


@router.get("/", response_model=List[personajeResponse])
def get_personaje(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).offset(skip).limit(limit).all()
    return personaje

@router.post("/create", response_model=personajeResponse)
def create_personaje(personaje: personajeCreate, db: Session = Depends(get_db)):
    new_personaje = Personaje(**personaje.dict())
    db.add(new_personaje)
    db.commit()
    db.refresh(new_personaje)
    return new_personaje

@router.get("/{id_personaje}", response_model=personajeResponse)
def get_personaje(id_personaje: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.idpersonaje == id_personaje).first()
    if personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return personaje

@router.put("/{id_personaje}", response_model=personajeResponse)
def update_personaje(id_personaje: int, personaje: personajeCreate, db: Session = Depends(get_db)):
    db_personaje = db.query(Personaje).filter(Personaje.idpersonaje == id_personaje).first()
    if db_personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    
    for key, value in personaje.dict().items():
        setattr(db_personaje, key, value)
    
    db.commit()
    db.refresh(db_personaje)
    return db_personaje

@router.delete("/{id_personaje}", response_model=personajeResponse)
def delete_personaje(id_personaje: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.idpersonaje == id_personaje).first()
    if personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    
    db.delete(personaje)
    db.commit()
    return personaje
