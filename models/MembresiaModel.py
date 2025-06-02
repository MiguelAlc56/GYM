from pydantic import BaseModel
from datetime import date
from typing import Optional

class MembresiaInsert(BaseModel):
    Nombre: str
    Descripcion: str
    Precio: float
    Vigencia: int

class Salida(BaseModel):
    descripcion: str
    estatus: str

class MembresiaOut(BaseModel):
    idMembresias: int
    Nombre: str
    Descripcion: str
    Precio: float
    Vigencia: int

    class Config:
        from_attributes = True

class MembresiaUpdate(BaseModel):
    Nombre: Optional[str] = None
    Descripcion: Optional[str] = None
    Precio: Optional[float] = None
    Vigencia: Optional[int] = None

    class Config:
        from_attributes = True

class AsignacionMembresia(BaseModel):
    id_cliente: int
    id_membresia: int
    FechaInicio: date
    FechaFin: date
    Estatus: bool
    id_empleado: int

class DetalleMembresiaOut(BaseModel):
    idDetalleMembresia: int
    FechaInicio: date
    FechaFin: date
    Estatus: bool
    id_cliente: int
    id_membresia: int
    id_empleado: int
    membresia: MembresiaOut

    class Config:
        from_attributes = True

class MembresiaClienteOut(BaseModel):
    idDetalleMembresia: int
    FechaInicio: date
    FechaFin: date
    Estatus: bool
    cliente_id: int
    membresia: MembresiaOut

    class Config:
        from_attributes = True