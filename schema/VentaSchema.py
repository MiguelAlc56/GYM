from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base
from .EmpleadosSchema import Empleado
from dao.database import Base

#Base = declarative_base()

class Venta(Base):
    __tablename__ = "venta"
    idVenta = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("empleados.idEmpleados"), nullable=False)
    fecha = Column(Date, nullable=False)
    total = Column(Float, nullable=False)
    comentarios = Column(String(255))

    detalles = relationship("DetalleVenta")
    usuario = relationship("Empleado")
#Venta.usuario = relationship("Empleado")