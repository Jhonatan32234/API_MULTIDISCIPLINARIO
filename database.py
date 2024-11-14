from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
#NOTA AL FINAL DE LA URL TIENE DEFINIDO postgres ESTE SERA LA BASE
# DE DATOS EN LA CUAL ESTA EL ESQUEMA EL CUAL CONTIENE LAS TABLAS

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_POSTGRESQL_URL")



#DATABASE_URL = "postgresql://postgres:@localhost:5432/proyectos?options=-c%20client_encoding=WIN1252"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
