# main.py
from fastapi import FastAPI

#POSTGRESQL
from postgresql.database import engine
import postgresql.models as models 
from postgresql.routes.nivel import router as nivel_router
from postgresql.routes.configuracion import router as configuracion_router
from postgresql.routes.progreso import router as progreso_router
from postgresql.routes.usuario import router as usuario_router
#MONGODB
from mongo.routes.terminal import router as terminal_router
from mongo.routes.bloqueCodigo import router as bloquecodigo_router
from mongo.routes.terminalCodigo import router as terminalcodigo_router
from mongo.routes.pared import router as pared_router
from mongo.routes.personaje import router as personaje_router
from mongo.routes.puente import router as puente_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#POSTGRESQL
models.Base.metadata.create_all(bind=engine)

app.include_router(nivel_router,prefix="/nivel",tags=["Nivel"])
app.include_router(usuario_router,prefix="/usuario",tags=["Usuario"])
app.include_router(progreso_router,prefix="/progreso",tags=["Progreso"])
app.include_router(configuracion_router,prefix="/configuracion",tags=["Configuracion"])

#MONGODB
app.include_router(pared_router, prefix="/pared", tags=["Pared"])
app.include_router(personaje_router, prefix="/personaje", tags=["Personaje"])
app.include_router(puente_router, prefix="/puente", tags=["Puente"])
app.include_router(terminal_router, prefix="/terminal", tags=["Terminal"])
app.include_router(bloquecodigo_router, prefix="/bloqueCodigo", tags=["bloqueCodigo"])
app.include_router(terminalcodigo_router, prefix="/terminalCodigo", tags=["terminalCodigo"])
