# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from postgresql.database import get_db
from postgresql.models import Nivel, Progreso
from postgresql.schemas import nivelCreate, nivelResponse
from access.jwt_access import verify_role


router = APIRouter()

#obtener todos los niveles
@router.get("/", response_model=List[nivelResponse])
def get_nivel(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    user: dict = verify_role(["usuario","admin"]) 
    ):
    nivel = db.query(Nivel).offset(skip).limit(limit).all()
    return nivel

#crear un nivel
@router.post("/create", response_model=nivelResponse)
def create_nivel(
    nivel: nivelCreate, 
    db: Session = Depends(get_db),
    #user: dict = verify_role(["admin"]) 
    ):
    new_nivel = Nivel(**nivel.dict())
    db.add(new_nivel)
    db.commit()
    db.refresh(new_nivel)
    return new_nivel

#obterner un nivel especifico
@router.get("/{id_nivel}", response_model=nivelResponse)
def get_nivel(
    id_nivel: int,
      db: Session = Depends(get_db),
      user: dict = verify_role(["admin","usuario"]) 
      ):
    nivel = db.query(Nivel).filter(Nivel.idnivel == id_nivel).first()
    if nivel is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return nivel

#actualizar un nivel
@router.put("/{id_nivel}", response_model=nivelResponse)
def update_nivel(
    id_nivel: int, 
    nivel: nivelCreate, 
    db: Session = Depends(get_db),
    user: dict = verify_role(["admin"]) 
    ):
    db_nivel = db.query(Nivel).filter(Nivel.idnivel == id_nivel).first()
    if db_nivel is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    
    for key, value in nivel.dict().items():
        setattr(db_nivel, key, value)
    
    db.commit()
    db.refresh(db_nivel)
    return db_nivel

#eliminar un nivel
@router.delete("/{id_nivel}", response_model=nivelResponse)
def delete_nivel(
    id_nivel: int,
    db: Session = Depends(get_db),
    user: dict = verify_role(["admin"]) 
    ):
    nivel = db.query(Nivel).filter(Nivel.idnivel == id_nivel).first()
    if nivel is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    
    db.delete(nivel)
    db.commit()
    return nivel

#obtener todos los niveles con el añadido de mostrar cuales niveles tiene desbloqueado el usuario
@router.get("/niveles_usuario/{id_usuario}", response_model=List[dict])
def get_niveles_con_progreso(
    id_usuario: int, 
    db: Session = Depends(get_db),
    user: dict = verify_role(["admin","usuario"]) 
    ):
    # Obtener todos los niveles
    niveles = db.query(Nivel).all()
    if not niveles:
        raise HTTPException(status_code=404, detail="No se encontraron niveles")

    # Consultar los progresos del usuario
    progresos_usuario = db.query(Progreso).filter(Progreso.idusuario == id_usuario).all()
    niveles_completados = {progreso.idnivel for progreso in progresos_usuario}

    # Construir respuesta con el estado de progreso
    resultado = [
        {
            "idnivel": nivel.idnivel,
            "nombrenivel": nivel.nombrenivel,
            "textura": nivel.textura,
            "desbloqueado": nivel.idnivel in niveles_completados
        }
        for nivel in niveles
    ]

    return resultado