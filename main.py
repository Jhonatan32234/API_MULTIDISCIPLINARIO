# main.py
from fastapi import FastAPI
from database import engine
import models 
""""
from routes.ejemplos.materias import router as materias_router
from routes.ejemplos.trabajador import router as trabajadores_router
from routes.ejemplos.proyecto import router as proyectos_router
from routes.ejemplos.proyectoAsignado import router as proyectos_asignados
from routes.ejemplos.jefe import router as jefes_router"""

from routes.terminal import router as terminal_router
from routes.bloqueCodigo import router as bloquecodigo_router
from routes.terminalCodigo import router as terminalcodigo_router
from routes.nivel import router as nivel_router
from routes.pared import router as pared_router
from routes.personaje import router as personaje_router
from routes.puente import router as puente_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI();

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


models.Base.metadata.create_all(bind=engine)

app.include_router(nivel_router,prefix="/nivel",tags=["Nivel"])
app.include_router(pared_router,prefix="/pared",tags=["Pared"])
app.include_router(personaje_router,prefix="/personaje",tags=["Personaje"])
app.include_router(puente_router,prefix="/puente",tags=["Puente"])
app.include_router(terminal_router,prefix="/terminal",tags=["Terminal"])
app.include_router(bloquecodigo_router,prefix="/bloqueCodigo",tags=["bloqueCodigo"])
app.include_router(terminalcodigo_router,prefix="/terminalCodigo",tags=["terminalCodigo"])






""""
app.include_router(materias_router,prefix="/materias",tags=["Materias"])
app.include_router(trabajadores_router,prefix="/trabajadores",tags=["Trabajadores"])
app.include_router(jefes_router,prefix="/jefe",tags=["Jefe de Proyecto"])
app.include_router(proyectos_asignados,prefix="/proyectos_asignados",tags=["Proyectos Asignados"])
app.include_router(proyectos_router,prefix="/proyectos",tags=["Proyectos"])"""