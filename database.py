from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

#NOTA AL FINAL DE LA URL TIENE DEFINIDO postgres ESTE SERA LA BASE
# DE DATOS EN LA CUAL ESTA EL ESQUEMA EL CUAL CONTIENE LAS TABLAS
DATABASE_URL = "postgresql://postgres:contrasena@184.72.254.221:5432/postgres"  # Cambia por tus credenciales

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
