from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base
from dao.database import Base
#from .VentaSchema import Base
#from .ProductoSchema import Base

#Base = declarative_base()

class DetalleVenta(Base):
    __tablename__ = "detalleventa"
    id_venta = Column(Integer, ForeignKey("venta.idVenta"), primary_key=True)
    id_producto = Column(Integer, ForeignKey("productos.idproductos"), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    venta = relationship("Venta")
    producto = relationship("Producto")
