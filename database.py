from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

#NOTA AL FINAL DE LA URL TIENE DEFINIDO postgres ESTE SERA LA BASE
# DE DATOS EN LA CUAL ESTA EL ESQUEMA EL CUAL CONTIENE LAS TABLAS
#DATABASE_URL = "postgresql://multidisciplinario:codebox@54.164.45.73:5432/postgres"  # Cambia por tus credenciales



DATABASE_URL = "postgresql://postgres:@localhost:5432/proyectos?options=-c%20client_encoding=WIN1252"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
