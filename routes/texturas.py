# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Texturas
from schemas import texturasCreate, texturaResponse

router = APIRouter()


@router.get("/", response_model=List[texturaResponse])
def get_textura(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    textura = db.query(Texturas).offset(skip).limit(limit).all()
    return textura

@router.post("/create", response_model=texturaResponse)
def create_textura(textura: texturasCreate, db: Session = Depends(get_db)):
    new_textura = Texturas(**textura.dict())
    db.add(new_textura)
    db.commit()
    db.refresh(new_textura)
    return new_textura

@router.get("/{id_textura}", response_model=texturaResponse)
def get_textura(id_textura: int, db: Session = Depends(get_db)):
    textura = db.query(Texturas).filter(Texturas.idtextura == id_textura).first()
    if textura is None:
        raise HTTPException(status_code=404, detail="Textura no encontrado")
    return textura

@router.put("/{id_textura}", response_model=texturaResponse)
def update_textura(id_textura: int, textura: texturasCreate, db: Session = Depends(get_db)):
    db_textura = db.query(Texturas).filter(Texturas.idtextura == id_textura).first()
    if db_textura is None:
        raise HTTPException(status_code=404, detail="Textura no encontrado")
    
    for key, value in textura.dict().items():
        setattr(db_textura, key, value)
    
    db.commit()
    db.refresh(db_textura)
    return db_textura

@router.delete("/{id_textura}", response_model=texturaResponse)
def delete_textura(id_textura: int, db: Session = Depends(get_db)):
    textura = db.query(Texturas).filter(Texturas.idtextura == id_textura).first()
    if textura is None:
        raise HTTPException(status_code=404, detail="Textura no encontrado")
    
    db.delete(textura)
    db.commit()
    return textura
