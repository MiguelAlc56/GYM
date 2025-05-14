from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dao.EmpleadosDAO import insertar_empleado, obtener_empleado_por_id, obtener_todos_los_empleados,actualizar_empleado,eliminar_empleado
from dao.database import get_db

from models.EmpleadosModel import empleadoInsert, Salida, EmpleadoOut, EmpleadoUpdate
from models.PersonaModel import Persona

router = APIRouter(
    prefix="/empleados",
    tags=["Empleados"]
)

@router.post("/agregar", response_model=Salida)
async def crearEmpleado(empleado: empleadoInsert, db: Session = Depends(get_db))->Salida:
    nuevo_empleado = insertar_empleado(db, empleado)
    return nuevo_empleado

@router.get("/obtener/{id_empleado}", response_model=EmpleadoOut)
def get_empleado(id_empleado: int, db: Session = Depends(get_db)):
    empleado = obtener_empleado_por_id(db, id_empleado)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@router.get("/obtenerTodos", response_model=List[EmpleadoOut])
def get_todos_los_empleados(db: Session = Depends(get_db)):
    empleados = obtener_todos_los_empleados(db)
    return empleados

@router.put("/actualizar/{id_empleado}", response_model=Salida)
def update_empleado(id_empleado: int, empleado_update: EmpleadoUpdate, db: Session = Depends(get_db))->Salida:
    empleado_actualizado = actualizar_empleado(db, id_empleado, empleado_update)
    return empleado_actualizado

@router.delete("/eliminar/{id_empleado}", response_model=Salida)
def delete_empleado(id_empleado: int, db: Session = Depends(get_db)):
    eliminado = eliminar_empleado(db, id_empleado)
    return eliminado