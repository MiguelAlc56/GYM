from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Persona(Base):
    __tablename__ = 'persona'

    idPersona = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(45), nullable=False)
    Apellido = Column(String(45), nullable=False)
    FechaNacimineto = Column(Date, nullable=False)
    Telefono = Column(String(10), nullable=False)
    Correo = Column(String(45), nullable=False)
    Sexo = Column(String(1), nullable=False)
