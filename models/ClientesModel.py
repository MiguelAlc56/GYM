from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class clienteInsert(BaseModel):
    Nombre: str
    Apellido: str
    FechaNacimineto: date
    Telefono: str
    Correo: str
    Sexo: str
    Fecha_Adquisicion: date
    Estatus: str

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

class ClienteOut(BaseModel):
    idClientes: int
    Fecha_Adquisicion: date
    Estatus: str
    id_persona: int
    persona: PersonaOut

    class Config:
        from_attributes = True

#Optional para que el usuario pueda ingresar unicamente los datos a cambiar
class ClienteUpdate(BaseModel):
    Nombre: Optional[str] = None
    Apellido: Optional[str] = None
    FechaNacimineto: Optional[date] = None
    Telefono: Optional[str] = None
    Correo: Optional[str] = None
    Sexo: Optional[str] = None
    Fecha_Adquisicion: Optional[date] = None
    Estatus: Optional[str] = None

    class Config:
        from_attributes = True

