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
    nombreusuario: int
    contrasena:str
    idconfiguracion:int


class usuarioResponse(usuarioCreate):
    idusuario:int

    class Config:
        orm_mode = True

class configuracionCreate(BaseModel):
    musica:bool
    fxsounds:bool
    controles:str

class configuracionResponse(configuracionCreate):
    idconfiguracion:int

    class Config:
        orm_mode = True

class progresoCreate(BaseModel):
    idnivel:int
    idusuario:int

class progresoResponse(progresoCreate):
    idprogreso:int

    class Config:
        orm_mode = True


