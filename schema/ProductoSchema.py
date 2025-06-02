from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dao.database import Base
from .ProveedoresSchema import Proveedor

class Producto(Base):
    __tablename__ = "productos"
    idproductos = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    categoria = Column(String(100))
    precio = Column(Float, nullable=False)
    existencias = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedores.idproveedores"))

    proveedor = relationship("Proveedor")
