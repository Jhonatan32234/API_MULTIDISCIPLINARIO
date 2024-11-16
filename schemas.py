from pydantic import BaseModel
from typing import List, Optional
from datetime import date



class nivelCreate(BaseModel):
    nombrenivel: str
    textura: str

class nivelResponse(nivelCreate):
    idnivel: int
    
    class Config:
        orm_mode = True

class usuarioCreate(BaseModel):
    nombreusuario: str
    contrasena:str
    idconfiguracion:Optional[int] = None


class usuarioResponse(usuarioCreate):
    idusuario:int

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    nombreusuario: str
    contrasena: str

class configuracionCreate(BaseModel):
    musica:bool
    fxsounds:bool
    controles:str

class configuracionResponse(configuracionCreate):
    idconfiguracion:int

    class Config:
        orm_mode = True

class progresoCreate(BaseModel):
    idnivel:Optional[int] = None
    idusuario:Optional[int] = None

class progresoResponse(progresoCreate):
    idprogreso:int

    class Config:
        orm_mode = True


