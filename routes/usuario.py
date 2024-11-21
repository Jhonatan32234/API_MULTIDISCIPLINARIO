# routes/materias.py
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException,Response
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Usuario, Configuracion, Progreso, Nivel
from schemas import usuarioCreate, usuarioResponse, LoginRequest
import bcrypt
import os
from dotenv import load_dotenv
from access.jwt_access import create_access_token
from fastapi.responses import JSONResponse
from access.jwt_access import get_token
from access.jwt_access import verify_role

load_dotenv()

router = APIRouter()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

@router.get("/", response_model=List[usuarioResponse])
def get_usuario(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: dict = verify_role("admin")  # Valida token y verifica el rol "admin"
):
    usuario = db.query(Usuario).offset(skip).limit(limit).all()
    return usuario



@router.get("/{id_usuario}", response_model=usuarioResponse)
def get_usuario(id_usuario: int, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    usuario = db.query(Usuario).filter(Usuario.idusuario == id_usuario).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{id_usuario}", response_model=usuarioResponse)
def update_usuario(id_usuario: int, usuario: usuarioCreate, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    db_usuario = db.query(Usuario).filter(Usuario.idusuario == id_usuario).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/{id_usuario}", response_model=usuarioResponse)
def delete_usuario(id_usuario: int, db: Session = Depends(get_db),user:dict = Depends(get_token)):
    usuario = db.query(Usuario).filter(Usuario.idusuario == id_usuario).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return usuario


@router.post("/login")
def login_usuario(request: LoginRequest, db: Session = Depends(get_db)):
    # Verificar si el usuario existe en la base de datos
    usuario = db.query(Usuario).filter(Usuario.nombreusuario == request.nombreusuario).first()

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario o contraseña incorrecta")

    # Verificar la contraseña
    if not bcrypt.checkpw(request.contrasena.encode('utf-8'), usuario.contrasena.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrecta")

    # Crear el token de acceso
    access_token = create_access_token(
        data={"sub": usuario.nombreusuario, "rol": usuario.rol}
    )

    # Crear la información del usuario para el cuerpo de la respuesta JSON
    usuario_dict = {
        "idusuario": usuario.idusuario,
        "nombreusuario": usuario.nombreusuario,
        "idconfiguracion": usuario.idconfiguracion,
        "rol": usuario.rol
    }

    # Crear la respuesta JSON con encabezados personalizados
    response = JSONResponse(content=usuario_dict, status_code=200)
    response.headers["Authorization"] = f"Bearer {access_token}"

    return response


@router.post("/register")
def register_usuario(usuario: usuarioCreate, db: Session = Depends(get_db)):
    nueva_configuracion = Configuracion(
        musica=True,         
        fxsounds=True,      
        controles="default"  
    )
    db.add(nueva_configuracion)
    db.commit()
    db.refresh(nueva_configuracion)

    hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())

    new_usuario = Usuario(
        nombreusuario=usuario.nombreusuario,
        contrasena=hashed_password.decode('utf-8'), 
        idconfiguracion=nueva_configuracion.idconfiguracion,
        rol=usuario.rol 
    )
    db.add(new_usuario)
    db.commit()  
    db.refresh(new_usuario)

    primer_nivel = db.query(Nivel).first() 
    if not primer_nivel:
        raise HTTPException(status_code=404, detail="Nivel inicial no encontrado")

    nuevo_progreso = Progreso(
        idnivel=primer_nivel.idnivel,
        idusuario=new_usuario.idusuario
    )
    db.add(nuevo_progreso)
    db.commit()  
    db.refresh(nuevo_progreso)

    usuario_dict = {
        "idusuario": new_usuario.idusuario,
        "nombreusuario": new_usuario.nombreusuario,
        "idconfiguracion": new_usuario.idconfiguracion,
        "rol": new_usuario.rol 
    }

    return usuario_dict


