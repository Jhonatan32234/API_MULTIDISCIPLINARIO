from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class bloqueCodigoCreate(BaseModel):
    ladox1: int
    ladox2: int
    ladoy1: int
    ladoy2: int
    idtextura: int

class bloqueCodigoResponse(bloqueCodigoCreate):
    idbloquecodigo: int

    class Config:
        orm_mode = True

class nivelCreate(BaseModel):
    nombrenivel: str
    tiempolimite: int
    idtextura: int

class nivelResponse(nivelCreate):
    idnivel: int
    
    class Config:
        orm_mode = True

class texturasCreate(BaseModel):
    archivotextura: str

class texturaResponse(texturasCreate):
    idtextura: int

    class Config:
        orm_mode = True

class personajeCreate(BaseModel):
    posicionx: int
    posiciony: int
    dimensionx: int
    dimensiony: int
    idtextura: int

class personajeResponse(personajeCreate):
    idpersonaje: int

    class Config:
        orm_mode = True

class paredCreate(BaseModel):
    ladox1: int
    ladox2: int
    ladoy1: int 
    ladoy2: int
    idtextura: int

class paredResponse(paredCreate):
    idpared: int

    class Config:
        orm_mode = True

class terminalCreate(BaseModel):
    ladox1: int
    ladox2: int
    ladoy1: int 
    ladoy2: int
    idtextura: int
    idpuente: int

class terminalResponse(terminalCreate):
    idterminal: int

    class Config:
        orm_mode = True

class terminalCodigoCreate(BaseModel):
    idterminal: int
    idcodigo: int

class terminalCodigoResponse(terminalCodigoCreate):
    idterminalcodigo: int

    class Config:
        orm_mode = True

class puenteCreate(BaseModel):
    ladox1: int
    ladox2: int
    ladoy1: int 
    ladoy2: int
    idtextura: int

class puenteResponse(puenteCreate):
    idpuente: int

    class Config:
        orm_mode = True
