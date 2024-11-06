
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base



class Nivel(Base):
    __tablename__ = "nivel"
    __table_args__ = {"schema":"multidisciplinario"}

    idnivel = Column(Integer,primary_key=True,index=True)
    nombrenivel = Column(String,index=True)
    tiempolimite = Column(Integer)



class Texturas(Base):
    __tablename__ = "texturas"
    __table_args__ =  {"schema":"multidisciplinario"}

    idtexura = Column(Integer,primary_key=True,index=True)
    archivotextura = Column(String)
    


class Personaje(Base):
    __tablename__ = "personaje"
    __table_args__ = {"schema":"multidisciplinario"}

    idpersonaje = Column(Integer,primary_key=True,index=True)
    posicionx = Column(Integer)
    posiciony = Column(Integer)


class Pared(Base):
    __tablename__ = "pared"
    __table_args__ = {"schema":"multidisciplinario"}
    
    idpared = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)


class Terminal(Base):
    __tablename__ = "terminal"
    __table_args__ = {"schema":"multidisciplinario"}

    idterminal = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)


class terminalCodigo(Base):
    __tablename__ = "terminalcodigo"
    __table_args__ = {"schema":"multidisciplinario"}

    idterminalcodigo = Column(Integer,primary_key=True,index=True)


class Puente(Base):
    __tablename__ = "Puente"
    __table_args__ = {"schema":"multidisciplinario"}

    idpuente = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)


class bloqueCodigo(Base):
    __tablename__ = "bloquecodigo"
    __table_args__ = {"schema":"multidisciplinario"}

    idbloquecodigo = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)




    
