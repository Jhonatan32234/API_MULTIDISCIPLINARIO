
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base



class Nivel(Base):
    __tablename__ = "nivel"
    __table_args__ = {"schema":"codebox"}

    idnivel = Column(Integer,primary_key=True,index=True)
    nombrenivel = Column(String,index=True)
    tiempolimite = Column(Integer)
    textura = Column(String)

    personaje = relationship("Personaje",back_populates="nivel")
    pared = relationship("Pared",back_populates="nivel")
    terminal = relationship("Terminal",back_populates="nivel")
    puente = relationship("Puente",back_populates="nivel")
    bloquecodigo = relationship("bloqueCodigo",back_populates="nivel")




"""class Texturas(Base):
    __tablename__ = "texturas"
    __table_args__ =  {"schema":"multidisciplinario"}

    idtextura = Column(Integer,primary_key=True,index=True)
    archivotextura = Column(String)

    niveltexturas = relationship("Nivel",back_populates="textura")
    personajetextura = relationship("Personaje",back_populates="textura")
    paredtextura = relationship("Pared",back_populates="textura")
    terminaltextura = relationship("Terminal",back_populates="textura")
    puentetextura = relationship("Puente",back_populates="textura")
    bloquecodigotextura = relationship("bloqueCodigo",back_populates="textura")"""


class Personaje(Base):
    __tablename__ = "personaje"
    __table_args__ = {"schema":"codebox"}

    idpersonaje = Column(Integer,primary_key=True,index=True)
    posicionx = Column(Integer)
    posiciony = Column(Integer)
    dimensionx = Column(Integer)
    dimensiony = Column(Integer)
    textura = Column(String)
    idnivel = Column(Integer,ForeignKey("codebox.nivel.idnivel"))

    nivel = relationship("Nivel",back_populates="personaje")




class Pared(Base):
    __tablename__ = "pared"
    __table_args__ = {"schema":"codebox"}
    
    idpared = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)
    textura = Column(String)

    idnivel = Column(Integer,ForeignKey("codebox.nivel.idnivel"))

    nivel = relationship("Nivel",back_populates="pared")


class Terminal(Base):
    __tablename__ = "terminal"
    __table_args__ = {"schema":"codebox"}

    idterminal = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)
    textura = Column(String)

    idpuente = Column(Integer,ForeignKey("codebox.puente.idpuente"))
    idnivel = Column(Integer,ForeignKey("codebox.nivel.idnivel"))


    puente = relationship("Puente",back_populates="terminal")
    tmcodigo = relationship("terminalCodigo",back_populates="terminal")
    nivel = relationship("Nivel",back_populates="terminal")

    


class terminalCodigo(Base):
    __tablename__ = "terminalcodigo"
    __table_args__ = {"schema":"codebox"}

    idterminalcodigo = Column(Integer,primary_key=True,index=True)
    idterminal = Column(Integer,ForeignKey("codebox.terminal.idterminal"))
    idcodigo = Column(Integer,ForeignKey("codebox.bloquecodigo.idbloquecodigo"))

    terminal = relationship("Terminal",back_populates="tmcodigo")
    codigo = relationship("bloqueCodigo",back_populates="tmcodigo")


class Puente(Base):
    __tablename__ = "puente"
    __table_args__ = {"schema":"codebox"}

    idpuente = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)
    textura = Column(String)

    idnivel = Column(Integer,ForeignKey("codebox.nivel.idnivel"))


    terminal = relationship("Terminal",back_populates="puente")
    nivel = relationship("Nivel",back_populates="puente")




class bloqueCodigo(Base):
    __tablename__ = "bloquecodigo"
    __table_args__ = {"schema":"codebox"}

    idbloquecodigo = Column(Integer,primary_key=True,index=True)
    ladox1 = Column(Integer)
    ladox2 = Column(Integer)
    ladoy1 = Column(Integer)
    ladoy2 = Column(Integer)
    textura = Column(String)

    idnivel = Column(Integer,ForeignKey("codebox.nivel.idnivel"))

    tmcodigo = relationship("terminalCodigo",back_populates="codigo")
    nivel = relationship("Nivel",back_populates="bloquecodigo")





    
