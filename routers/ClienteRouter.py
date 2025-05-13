from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dao.ClientesDAO import insertar_cliente, obtener_cliente_por_id, obtener_todos_los_clientes, actualizar_cliente, eliminar_cliente
from dao.database import get_db

from models.ClientesModel import clienteInsert, Salida, ClienteOut, ClienteUpdate
from models.PersonaModel import Persona

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.post("/agregar", response_model=Salida)
async def crearCliente(cliente: clienteInsert, db: Session = Depends(get_db))->Salida:
    nuevo_cliente = insertar_cliente(db, cliente)
    return nuevo_cliente

@router.get("/obtener/{id_cliente}", response_model=ClienteOut)
def get_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente = obtener_cliente_por_id(db, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.get("/obtenerTodos", response_model=List[ClienteOut])
def get_todos_los_clientes(db: Session = Depends(get_db)):
    clientes = obtener_todos_los_clientes(db)
    return clientes

@router.put("/actualizar/{id_cliente}", response_model=Salida)
def update_cliente(id_cliente: int, cliente_update: ClienteUpdate, db: Session = Depends(get_db))->Salida:
    cliente_actualizado = actualizar_cliente(db, id_cliente, cliente_update)
    return cliente_actualizado

@router.delete("/eliminar/{id_cliente}", response_model=Salida)
def delete_cliente(id_cliente: int, db: Session = Depends(get_db)):
    eliminado = eliminar_cliente(db, id_cliente)
    return eliminado