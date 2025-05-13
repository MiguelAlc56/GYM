from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .PersonaSchema import Base, Persona

class Cliente(Base):
    __tablename__ = 'clientes'

    idClientes = Column(Integer, primary_key=True, autoincrement=True)
    Fecha_Adquisicion = Column(Date, nullable=False)
    Estatus = Column(String(45), nullable=False)
    id_persona = Column(Integer, ForeignKey('persona.idPersona'), nullable=False)

    persona = relationship("Persona")
