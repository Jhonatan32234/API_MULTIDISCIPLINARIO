# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Progreso
from schemas import progresoCreate, progresoResponse
from access.jwt_access import get_token

router = APIRouter()


@router.get("/", response_model=List[progresoResponse])
def get_progreso(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    progreso = db.query(Progreso).offset(skip).limit(limit).all()
    return progreso

@router.post("/create", response_model=progresoResponse)
def create_progreso(progreso: progresoCreate, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    new_progreso = Progreso(**progreso.dict())
    db.add(new_progreso)
    db.commit()
    db.refresh(new_progreso)
    return new_progreso

@router.get("/{id_progreso}", response_model=progresoResponse)
def get_progreso(id_progreso: int, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    progreso = db.query(Progreso).filter(Progreso.idprogreso == id_progreso).first()
    if progreso is None:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso

@router.put("/{id_progreso}", response_model=progresoResponse)
def update_progreso(id_progreso: int, progreso: progresoCreate, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    db_progreso = db.query(Progreso).filter(Progreso.idprogreso == id_progreso).first()
    if db_progreso is None:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    
    for key, value in progreso.dict().items():
        setattr(db_progreso, key, value)
    
    db.commit()
    db.refresh(db_progreso)
    return db_progreso

@router.delete("/{id_progreso}", response_model=progresoResponse)
def delete_progreso(id_progreso: int, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    progreso = db.query(Progreso).filter(Progreso.idprogreso == id_progreso).first()
    if progreso is None:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    
    db.delete(progreso)
    db.commit()
    return progreso



@router.get("/nivel/{id_nivel}", response_model=progresoResponse)
def get_progreso(id_nivel: int, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    progreso = db.query(Progreso).filter(Progreso.idnivel == id_nivel).first()
    if progreso is None:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso

@router.get("/usuario/{id_usuario}", response_model=progresoResponse)
def get_progreso(id_usuario: int, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    progreso = db.query(Progreso).filter(Progreso.idusuario == id_usuario).first()
    if progreso is None:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso