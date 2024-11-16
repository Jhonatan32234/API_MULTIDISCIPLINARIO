# routes/materias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Usuario, Configuracion, Progreso, Nivel
from schemas import usuarioCreate, usuarioResponse, LoginRequest

router = APIRouter()


@router.get("/", response_model=List[usuarioResponse])
def get_usuario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).offset(skip).limit(limit).all()
    return usuario

@router.post("/register", response_model=usuarioResponse)
def create_usuario(usuario: usuarioCreate, db: Session = Depends(get_db)):
    # Crear una configuración predeterminada para el usuario
    nueva_configuracion = Configuracion(
        musica=True,         # Valor por defecto para música
        fxsounds=True,       # Valor por defecto para efectos de sonido
        controles="default"  # Valor por defecto para controles
    )
    db.add(nueva_configuracion)
    db.commit()
    db.refresh(nueva_configuracion)

    # Crear el nuevo usuario y asociarlo a la configuración
    new_usuario = Usuario(
        nombreusuario=usuario.nombreusuario,
        contrasena=usuario.contrasena,
        idconfiguracion=nueva_configuracion.idconfiguracion
    )
    db.add(new_usuario)
    db.commit()  # Confirma para que el usuario tenga un ID
    db.refresh(new_usuario)

    # Crear un progreso asociado al primer nivel para el usuario
    primer_nivel = db.query(Nivel).first()  # Obtener el primer nivel disponible
    if not primer_nivel:
        raise HTTPException(status_code=404, detail="Nivel inicial no encontrado")

    nuevo_progreso = Progreso(
        idnivel=primer_nivel.idnivel,
        idusuario=new_usuario.idusuario
    )
    db.add(nuevo_progreso)
    db.commit()  # Confirma el progreso
    db.refresh(nuevo_progreso)

    return new_usuario


@router.get("/{id_usuario}", response_model=usuarioResponse)
def get_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.idusuario == id_usuario).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{id_usuario}", response_model=usuarioResponse)
def update_usuario(id_usuario: int, usuario: usuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.idusuario == id_usuario).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/{id_usuario}", response_model=usuarioResponse)
def delete_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.idusuario == id_usuario).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return usuario


@router.post("/login", response_model=usuarioResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.nombreusuario == request.nombreusuario,
        Usuario.contrasena == request.contrasena
    ).first()
    
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario o contraseña incorrectos")
    
    return usuario