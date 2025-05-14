from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .PersonaSchema import Base, Persona

class Empleado(Base):
    __tablename__ = 'empleados'

    idEmpleados = Column(Integer, primary_key=True, autoincrement=True)
    Contraseña=Column(String(45),nullable=False)
    Roll=Column(String(45),nullable=False)
    Estatus = Column(String(45), nullable=False)
    id_persona = Column(Integer, ForeignKey('persona.idPersona'), nullable=False)

    persona = relationship("Persona")
