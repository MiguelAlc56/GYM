from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class empleadoInsert(BaseModel):
    Nombre: str
    Apellido: str
    FechaNacimineto: date
    Telefono: str
    Correo: str
    Sexo: str
    Contraseña :str
    Roll:str|None='Recepcionsta'
    Estaus:str|None='Activo'

class Salida(BaseModel):
    descripcion: str
    estatus: str


class PersonaOut(BaseModel):
    idPersona: int
    Nombre: str
    Apellido: str
    FechaNacimineto: date
    Telefono: str
    Correo: str
    Sexo: str

    class Config:
        from_attributes = True


class EmpleadoOut(BaseModel):
    idEmpleados: int
    Contraseña: str
    Roll:str
    Estatus: str
    id_persona: int
    persona: PersonaOut

    class Config:
        from_attributes = True

class EmpleadoUpdate(BaseModel):
    Nombre: Optional[str] = None
    Apellido: Optional[str] = None
    FechaNacimineto: Optional[date] = None
    Telefono: Optional[str] = None
    Correo: Optional[str] = None
    Sexo: Optional[str] = None
    Contraseña:Optional[str]=None
    Roll:Optional[str]=None
    Estatus: Optional[str] = None

    class Config:
        from_attributes = True
