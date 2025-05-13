from pydantic import BaseModel
from datetime import datetime, date

class Persona(BaseModel):
    nombre: str
    apellido: str
    fechaNacimiento: date
    telefono: str
    correo: str
    sexo: str

