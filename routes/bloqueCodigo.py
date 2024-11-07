# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import bloqueCodigo
from schemas import bloqueCodigoCreate, bloqueCodigoResponse

router = APIRouter()


@router.get("/", response_model=List[bloqueCodigoResponse])
def get_bloquecodigo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bloquecodigo = db.query(bloqueCodigo).offset(skip).limit(limit).all()
    return bloquecodigo

@router.post("/create", response_model=bloqueCodigoResponse)
def create_bloquecodigo(bloquecodigo: bloqueCodigoCreate, db: Session = Depends(get_db)):
    new_bloquecodigo = bloqueCodigo(**bloquecodigo.dict())
    db.add(new_bloquecodigo)
    db.commit()
    db.refresh(new_bloquecodigo)
    return new_bloquecodigo

@router.get("/{id_bloquecodigo}", response_model=bloqueCodigoResponse)
def get_bloquecodigo(id_bloquecodigo: int, db: Session = Depends(get_db)):
    bloquecodigo = db.query(bloqueCodigo).filter(bloqueCodigo.idbloquecodigo == id_bloquecodigo).first()
    if bloquecodigo is None:
        raise HTTPException(status_code=404, detail="bloqueCodigo no encontrado")
    return bloquecodigo

@router.put("/{id_bloquecodigo}", response_model=bloqueCodigoResponse)
def update_bloquecodigo(id_bloquecodigo: int, bloquecodigo: bloqueCodigoCreate, db: Session = Depends(get_db)):
    db_bloquecodigo = db.query(bloqueCodigo).filter(bloqueCodigo.idbloquecodigo == id_bloquecodigo).first()
    if db_bloquecodigo is None:
        raise HTTPException(status_code=404, detail="bloqueCodigo no encontrado")
    
    for key, value in bloquecodigo.dict().items():
        setattr(db_bloquecodigo, key, value)
    
    db.commit()
    db.refresh(db_bloquecodigo)
    return db_bloquecodigo

@router.delete("/{id_bloquecodigo}", response_model=bloqueCodigoResponse)
def delete_bloquecodigo(id_bloquecodigo: int, db: Session = Depends(get_db)):
    bloquecodigo = db.query(bloqueCodigo).filter(bloqueCodigo.idbloquecodigo == id_bloquecodigo).first()
    if bloquecodigo is None:
        raise HTTPException(status_code=404, detail="bloqueCodigo no encontrado")
    db.delete(bloquecodigo)
    db.commit()
    return bloquecodigo
