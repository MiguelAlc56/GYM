from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from dao.database import Base
from .ClientesSchema import Cliente
from .EmpleadosSchema import Empleado


class Membresia(Base):
    __tablename__ = 'membresias'

    idMembresias = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(45), nullable=False)
    Descripcion = Column(String(255), nullable=False)
    Precio = Column(Float, nullable=False)
    Vigencia = Column(Integer, nullable=False)  # en días

    # Relación con los clientes que tienen esta membresía
    #clientes = relationship("DetalleMembresia")
