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

from routes.nivel import router as nivel_router
from routes.configuracion import router as configuracion_router
from routes.progreso import router as progreso_router
from routes.usuario import router as usuario_router



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
app.include_router(usuario_router,prefix="/usuario",tags=["Usuario"])
app.include_router(progreso_router,prefix="/progreso",tags=["Progreso"])
app.include_router(configuracion_router,prefix="/configuracion",tags=["Configuracion"])

