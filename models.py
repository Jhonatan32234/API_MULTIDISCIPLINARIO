
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base



class Nivel(Base):
    __tablename__ = "nivel"
    __table_args__ = {"schema":"codebox"}

    idnivel = Column(Integer,primary_key=True,index=True)
    nombrenivel = Column(String,index=True)
    textura = Column(String)

    progreso = relationship("Progreso",back_populates="nivel")


class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = {"schema":"codebox"}

    idusuario= Column(Integer,primary_key=True,index=True)
    nombreusuario = Column(String)
    contrasena = Column(String)
    idconfiguracion = Column(Integer,ForeignKey("codebox.configuracion.idconfiguracion"),nullable=True)
    rol = Column(String,default="usuario")

    progreso = relationship("Progreso",back_populates="usuario")
    configuracion = relationship("Configuracion",back_populates="usuario")
 


class Progreso(Base):
    __tablename__ = "progreso"
    __table_args__ = {"schema":"codebox"}

    idprogreso= Column(Integer,primary_key=True,index=True)
    idnivel = Column(Integer,ForeignKey("codebox.nivel.idnivel"),nullable=True)
    idusuario = Column(Integer,ForeignKey("codebox.usuario.idusuario"),nullable=True)

    usuario = relationship("Usuario",back_populates="progreso")
    nivel = relationship("Nivel",back_populates="progreso")

class Configuracion(Base):
    __tablename__ = "configuracion"
    __table_args__ = {"schema":"codebox"}

    idconfiguracion = Column(Integer,primary_key=True,index=True)
    musica = Column(Boolean)
    fxsounds = Column(Boolean)
    controles = Column(String)

    usuario = relationship("Usuario",back_populates="configuracion")

