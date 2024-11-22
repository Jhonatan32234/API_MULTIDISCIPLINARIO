from pydantic import BaseModel
from typing import Optional


# Usamos Pydantic para definir las validaciones
class Personaje(BaseModel):
    posicionx: int
    posiciony: int
    dimensionx: int
    dimensiony: int
    textura: str
    idnivel: int

    class Config:
        orm_mode = True

class Pared(BaseModel):
    ladox1: int
    ladox2: int
    ladoy1: int
    ladoy2: int
    textura: str
    idnivel: int

    class Config:
        orm_mode = True

class Puente(BaseModel):
    ladox1: int
    ladox2: int
    ladoy1: int
    ladoy2: int
    textura: str
    idnivel: int

    class Config:
        orm_mode = True

class Terminal(BaseModel):
    ladox1: int
    ladox2: int
    ladoy1: int
    ladoy2: int
    textura: str
    idpuente: int
    idnivel: int

    class Config:
        orm_mode = True

class BloqueCodigo(BaseModel):
    ladox1: int
    ladox2: int
    ladoy1: int
    ladoy2: int
    textura: str
    idnivel: int

    class Config:
        orm_mode = True

class TerminalCodigo(BaseModel):
    idterminal: int
    idcodigo: int

    class Config:
        orm_mode = True
