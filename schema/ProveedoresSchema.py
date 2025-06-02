from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from dao.database import Base


class Proveedor(Base):
    __tablename__ = "proveedores"
    idproveedores = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    contacto = Column(String(100))
    telefono = Column(String(11))
    direccion = Column(String(255))
    