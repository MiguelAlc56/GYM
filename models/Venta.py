from typing import List
from pydantic import BaseModel
from datetime import date

class DetalleVentaCreate(BaseModel):
    id_producto: int
    cantidad: int

class VentaCreate(BaseModel):
    id_usuario: int
    fecha: date
    comentarios: str | None = None
    productos: List[DetalleVentaCreate]

class Salida(BaseModel):
    descripcion: str
    estatus: str

class ComentarioUpdate(BaseModel):
    comentarios: str