
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base



class Nivel(Base):
    __tablename__ = "nivel"
    __table_args__ = {"schema":"multidisciplinario"}

    idnivel = Column(Integer,primary_key=True,index=True)
    nombrenivel = Column(String,index=True)
    tiempolimite = Column(Integer)

    idtextura = Column(Integer,ForeignKey("multidisciplinario.texturas.idtextura"),nullable=False)
    textura = relationship("Texturas",back_populates="niveltexturas")


class Texturas(Base):
    __tablename__ = "texturas"
    __table_args__ =  {"schema":"multidisciplinario"}

    idtexura = Column(Integer,primary_key=True,index=True)
    archivotextura = Column(String)

    niveltexturas = relationship("Nivel",back_populates="textura")
    personajetextura = relationship("Personaje",back_populates="textura")
    paredtextura = relationship("Pared",back_populates="textura")
    terminaltextura = relationship("Terminal",back_populates="textura")
    puentetextura = relationship("Puente",back_populates="textura")
    bloquecodigotextura = relationship("bloquecodigo",back_populates="textura")


class Personaje(Base):
    __tablename__ = "personaje"
    __table_args__ = {"schema":"multidisciplinario"}

    idpersonaje = Column(Integer,primary_key=True,index=True)
    posicionx = Column(Integer)
    posiciony = Column(Integer)
    dimensionx = Column(Integer)
    dimensiony = Column(Integer)

    idtextura = Column(Integer,ForeignKey("multidisciplinario.texturas.idtexura"))
    textura = relationship("Texturas",back_populates="personajetextura")


class Pared(Base):
    __tablename__ = "pared"
    __table_args__ = {"schema":"multidisciplinario"}
    
    idpared = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)

    idtextura = Column(Integer,ForeignKey("multidisciplinario.texturas.idtexura"))
    textura = relationship("Texturas",back_populates="paredtextura")



class Terminal(Base):
    __tablename__ = "terminal"
    __table_args__ = {"schema":"multidisciplinario"}

    idterminal = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)

    idtextura = Column(Integer,ForeignKey("multidisciplinario.texturas.idtexura"))
    idpuente = Column(Integer,ForeignKey("multidisciplinario.puente.idpuente"))

    textura = relationship("Texturas",back_populates="terminaltextura")
    puente = relationship("Puente",back_populates="terminal")
    tmcodigo = relationship("terminalcodigo",back_populates="terminal")
    


class terminalCodigo(Base):
    __tablename__ = "terminalcodigo"
    __table_args__ = {"schema":"multidisciplinario"}

    idterminalcodigo = Column(Integer,primary_key=True,index=True)
    idterminal = Column(Integer,ForeignKey("multidisciplinario.terminal.idterminal"))
    idcodigo = Column(Integer,ForeignKey("multidisciplinario.bloquecodigo.idbloquecodigo"))

    terminal = relationship("Terminal",back_populates="tmcodigo")
    codigo = relationship("bloquecodigo",back_populates="tmcodigo")


class Puente(Base):
    __tablename__ = "Puente"
    __table_args__ = {"schema":"multidisciplinario"}

    idpuente = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)

    idtextura = Column(Integer,ForeignKey("multidisciplinario.texturas.idtexura"))
    textura = relationship("Textura",back_populates="puentetextura")
    terminal = relationship("Terminal",back_populates="puente")



class bloqueCodigo(Base):
    __tablename__ = "bloquecodigo"
    __table_args__ = {"schema":"multidisciplinario"}

    idbloquecodigo = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)

    textura = relationship("Textura",back_populates="bloquecodigotextura")
    tmcodigo = relationship("terminalcodigo",back_populates="codigo")




    
