from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from dao.database import get_db
from models.Venta import VentaCreate, Salida, ComentarioUpdate
from dao.VentasDAO import crear_venta, actualizar_comentarios_venta, obtener_ventas_por_rango
from typing import List
from datetime import date

router = APIRouter(prefix="/ventas", tags=["ventas"])

@router.post("/crear", response_model=Salida)
def registrar_venta(venta: VentaCreate, db: Session = Depends(get_db))->Salida:
    nueva_venta = crear_venta(db, venta) 
    return nueva_venta

@router.put("/editar/{id_venta}", response_model=Salida)
def actualizar_comentarios(id_venta: int, datos: ComentarioUpdate, db: Session = Depends(get_db))->Salida:
    venta_actualizada = actualizar_comentarios_venta(db, id_venta, datos.comentarios)
    return venta_actualizada

@router.get("/reporte", response_model=List[dict])
def ventas_por_rango_fechas(
    fecha_inicio: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    if fecha_inicio > fecha_fin:
        raise HTTPException(status_code=400, detail="La fecha de inicio no puede ser mayor que la fecha de fin")

    ventas = obtener_ventas_por_rango(db, fecha_inicio, fecha_fin)
    if not ventas:
        return []

    resultado = []
    for venta in ventas:
        productos = []
        for detalle in venta.detalles:
            productos.append({
                "id_producto": detalle.id_producto,
                "producto": detalle.producto.nombre,
                "preciounitario": detalle.precio_unitario,
                "cantidad": detalle.cantidad,
                "subtotal": detalle.subtotal
            })

        resultado.append({
            "idVenta": venta.idVenta,
            "id_usuario": venta.id_usuario,
            "fecha": venta.fecha,
            "total": venta.total,
            "comentarios": venta.comentarios,
            "productos": productos
        })

    return resultado

    #return ventas