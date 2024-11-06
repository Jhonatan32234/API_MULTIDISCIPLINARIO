# schemas.py
from pydantic import BaseModel
from typing import List,Optional
from datetime import date

class MateriaBase(BaseModel):
    nom_materia: str
    creditos: int
    cant: int

class MateriaCreate(MateriaBase):
    pass

class MateriaResponse(MateriaBase):
    id_materia: int

    class Config:
        orm_mode = True


class JefeProyectoCreate(BaseModel):
    nombrejefe: str
    telefono: str
    correo: str
    aniosexperiencia: int
    salario: int

class JefeProyectoResponse(JefeProyectoCreate):
    idjefeproyecto: int

    class Config:
        orm_mode = True

class TrabajadorCreate(BaseModel):
    nombretrabajador: str
    posicion: str
    telefono: str
    correo: str
    salario: str
    aniosexperiencia: int

class TrabajadorResponse(TrabajadorCreate):
    idtrabajador: int

    class Config:
        orm_mode = True

class ProyectoCreate(BaseModel):
    nombreproyecto: str
    ubicacion: str
    fechainicio: date
    fechafinal: date
    presupuesto:int
    estadoproyecto: str
    idjefeproyecto: int

class ProyectoResponse(ProyectoCreate):
    idproyecto: int

    class Config:
        orm_mode = True

class ProyectoAsignadoCreate(BaseModel):
    idproyecto: int
    idtrabajador: int
    fechaasignacion: date
    horastrabajadas: int
    rolproyecto: str

class ProyectoAsignadoResponse(ProyectoAsignadoCreate):
    idproyectoasignado: int

    class Config:
        orm_mode = True