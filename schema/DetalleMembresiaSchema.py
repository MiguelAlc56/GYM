from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from dao.database import Base
from .ClientesSchema import Cliente
from .EmpleadosSchema import Empleado

class DetalleMembresia(Base):
    __tablename__ = 'detallemembresia'

    idDetalleMembresia = Column(Integer, primary_key=True, autoincrement=True)
    FechaInicio = Column(Date, nullable=False)
    FechaFin = Column(Date, nullable=False)
    Estatus = Column(Boolean, nullable=False)

    # Claves foráneas
    id_cliente = Column(Integer, ForeignKey('clientes.idClientes'), nullable=False)
    id_membresia = Column(Integer, ForeignKey('membresias.idMembresias'), nullable=False)
    id_empleado = Column(Integer, ForeignKey('empleados.idEmpleados'), nullable=False)

    # Relaciones
    cliente = relationship("Cliente")
    membresia = relationship("Membresia")
    empleado = relationship("Empleado")