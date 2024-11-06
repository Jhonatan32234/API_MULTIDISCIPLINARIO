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

from routes.texturas import router as texturas_router

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

app.include_router(texturas_router,prefix="/texturas",tags=["Texturas"])


""""
app.include_router(materias_router,prefix="/materias",tags=["Materias"])
app.include_router(trabajadores_router,prefix="/trabajadores",tags=["Trabajadores"])
app.include_router(jefes_router,prefix="/jefe",tags=["Jefe de Proyecto"])
app.include_router(proyectos_asignados,prefix="/proyectos_asignados",tags=["Proyectos Asignados"])
app.include_router(proyectos_router,prefix="/proyectos",tags=["Proyectos"])"""