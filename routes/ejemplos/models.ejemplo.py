# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Materia(Base):
    __tablename__ = "materias"
    __table_args__ = {"schema": "construccion"}

    id_materia = Column(Integer, primary_key=True, index=True)
    nom_materia = Column(String, index=True)
    creditos = Column(Integer)
    cant = Column(Integer)

class JefeProyecto(Base):
    __tablename__ = 'jefeproyecto'
    __table_args__ = {"schema": "construccion"}
    
    idjefeproyecto = Column(Integer, primary_key=True, index=True)
    nombrejefe = Column(String(100), nullable=False)
    telefono = Column(String(45), nullable=True)
    correo = Column(String(45), nullable=True)
    aniosexperiencia = Column(Integer, nullable=True)
    salario = Column(Integer, nullable=True)

    proyectos = relationship("Proyecto", back_populates="jefe")  # Actualizado

class Trabajador(Base):
    __tablename__ = 'trabajador'
    __table_args__ = {"schema": "construccion"}

    idtrabajador = Column(Integer, primary_key=True, index=True)
    nombretrabajador = Column(String(100), nullable=False)
    posicion = Column(String(50), nullable=True)
    telefono = Column(String(10), nullable=True)
    correo = Column(String(100), nullable=True)
    salario = Column(String(45), nullable=True)
    aniosexperiencia = Column(Integer, nullable=True)

    proyectos_asignados = relationship("ProyectoAsignado", back_populates="trabajador")  # Actualizado}
    

class Proyecto(Base):
    __tablename__ = 'proyecto'
    __table_args__ = {"schema": "construccion"}
    
    idproyecto = Column(Integer, primary_key=True, index=True)
    nombreproyecto = Column(String(150), nullable=False)
    ubicacion = Column(String(45), nullable=True)
    fechainicio = Column(Date, nullable=True)
    fechafinal = Column(Date, nullable=True)
    presupuesto = Column(Integer, nullable=True)
    estadoproyecto = Column(String(100), nullable=True)
    idjefeproyecto = Column(Integer, ForeignKey('construccion.jefeproyecto.idjefeproyecto'), nullable=True)  # Actualizado

    jefe = relationship("JefeProyecto", back_populates="proyectos")  # Actualizado
    proyectos_asignados = relationship("ProyectoAsignado", back_populates="proyecto")  # Actualizado

class ProyectoAsignado(Base):
    __tablename__ = 'proyectoasignado'
    __table_args__ = {"schema": "construccion"}
    
    idproyectoasignado = Column(Integer, primary_key=True, index=True)
    idproyecto = Column(Integer, ForeignKey('construccion.proyecto.idproyecto'), nullable=False)  # Actualizado
    idtrabajador = Column(Integer, ForeignKey('construccion.trabajador.idtrabajador'), nullable=False)  # Actualizado
    fechaasignacion = Column(Date, nullable=True)
    horastrabajadas = Column(Integer, nullable=True)
    rolproyecto = Column(String(100), nullable=True)

    proyecto = relationship("Proyecto", back_populates="proyectos_asignados")
    trabajador = relationship("Trabajador", back_populates="proyectos_asignados")
