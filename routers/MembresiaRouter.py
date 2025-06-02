from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dao.MembresiaDAO import (
    insertar_membresia,
    obtener_membresia_por_id,
    obtener_todas_las_membresias,
    actualizar_membresia,
    eliminar_membresia,
    asignar_membresia_cliente,
    obtener_membresias_cliente
)
from dao.database import get_db

from models.MembresiaModel import (
    MembresiaInsert,
    MembresiaOut,
    MembresiaUpdate,
    AsignacionMembresia,
    DetalleMembresiaOut,
    Salida
)

router = APIRouter(
    prefix="/membresias",
    tags=["Membresias"]
)

@router.post("/agregar", response_model=Salida)
async def crear_membresia(membresia: MembresiaInsert, db: Session = Depends(get_db)) -> Salida:
    nueva_membresia = insertar_membresia(db, membresia)
    return nueva_membresia

@router.get("/obtener/{id_membresia}", response_model=MembresiaOut)
def get_membresia(id_membresia: int, db: Session = Depends(get_db)):
    membresia = obtener_membresia_por_id(db, id_membresia)
    if not membresia:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")
    return membresia

@router.get("/obtenerTodos", response_model=List[MembresiaOut])
def get_todas_las_membresias(db: Session = Depends(get_db)):
    membresias = obtener_todas_las_membresias(db)
    return membresias

@router.put("/actualizar/{id_membresia}", response_model=Salida)
def update_membresia(id_membresia: int, membresia_update: MembresiaUpdate, db: Session = Depends(get_db)) -> Salida:
    membresia_actualizada = actualizar_membresia(db, id_membresia, membresia_update)
    return membresia_actualizada

@router.delete("/eliminar/{id_membresia}", response_model=Salida)
def delete_membresia(id_membresia: int, db: Session = Depends(get_db)):
    eliminado = eliminar_membresia(db, id_membresia)
    return eliminado

@router.post("/asignar", response_model=Salida)
async def asignar_membresia_a_cliente(asignacion: AsignacionMembresia, db: Session = Depends(get_db)) -> Salida:
    resultado = asignar_membresia_cliente(db, asignacion)
    return resultado

@router.get("/cliente/{id_cliente}", response_model=List[DetalleMembresiaOut])
def get_membresias_por_cliente(id_cliente: int, db: Session = Depends(get_db)):
    membresias = obtener_membresias_cliente(db, id_cliente)
    if not membresias:
        raise HTTPException(
            status_code=404,
            detail="El cliente no tiene membresías asignadas o no existe"
        )
    return membresias