# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from postgresql.database import get_db
from postgresql.models import Configuracion
from postgresql.schemas import configuracionCreate, configuracionResponse
from access.jwt_access import verify_role


router = APIRouter()

#obtener todas las configuraciones
@router.get("/", response_model=List[configuracionResponse])
def get_configuracion(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    user: dict = verify_role(["admin","usuario"]) 
    ):
    configuracion = db.query(Configuracion).offset(skip).limit(limit).all()
    return configuracion

#crear una configuracion
@router.post("/create", response_model=configuracionResponse)
def create_configuracion(
    configuracion: configuracionCreate, 
    db: Session = Depends(get_db),
    user: dict = verify_role(["admin"]) 
    ):
    new_configuracion = Configuracion(**configuracion.dict())
    db.add(new_configuracion)
    db.commit()
    db.refresh(new_configuracion)
    return new_configuracion

#obtener una configuracion especifica
@router.get("/{id_configuracion}", response_model=configuracionResponse)
def get_configuracion(
    id_configuracion: int, 
    db: Session = Depends(get_db),
    user: dict = verify_role(["admin","usuario"]) 
    ):
    configuracion = db.query(Configuracion).filter(Configuracion.idconfiguracion == id_configuracion).first()
    if configuracion is None:
        raise HTTPException(status_code=404, detail="Configuracion no encontrado")
    return configuracion

#actualizar una configuracion
@router.put("/{id_configuracion}", response_model=configuracionResponse)
def update_configuracion(
    id_configuracion: int, 
    configuracion: configuracionCreate, 
    db: Session = Depends(get_db),
    user: dict = verify_role(["admin"]) 
    ):
    db_configuracion = db.query(Configuracion).filter(Configuracion.idconfiguracion == id_configuracion).first()
    if db_configuracion is None:
        raise HTTPException(status_code=404, detail="Configuracion no encontrado")
    
    for key, value in configuracion.dict().items():
        setattr(db_configuracion, key, value)
    
    db.commit()
    db.refresh(db_configuracion)
    return db_configuracion

#eleminar una configuracion
@router.delete("/{id_configuracion}", response_model=configuracionResponse)
def delete_configuracion(
    id_configuracion: int, 
    db: Session = Depends(get_db),
    user: dict = verify_role(["admin"]) 
    ):
    configuracion = db.query(Configuracion).filter(Configuracion.idconfiguracion == id_configuracion).first()
    if configuracion is None:
        raise HTTPException(status_code=404, detail="Configuracion no encontrado")
    
    db.delete(configuracion)
    db.commit()
    return configuracion


