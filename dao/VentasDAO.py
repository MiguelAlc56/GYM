from sqlalchemy.orm import Session, joinedload
from schema.VentaSchema import Venta
from schema.Detalle_VentaSchema import DetalleVenta
from schema.ProductoSchema import Producto
from schema.EmpleadosSchema import Empleado
from models.Venta import VentaCreate, Salida
from fastapi import HTTPException
from datetime import date
from typing import List

def crear_venta(db: Session, venta_data: VentaCreate):
    salida = Salida(descripcion="", estatus="")
    try:
        empleado = db.query(Empleado).filter(Empleado.idEmpleados == venta_data.id_usuario).first()
        if not empleado:
            #raise HTTPException(status_code=404, detail="Empleado no encontrado")
            salida.descripcion = "Empleado no encontrado"
            salida.estatus = "Error"
            return salida
        if empleado.Roll.lower() != "recepcionista":
            #raise HTTPException(status_code=403, detail="Solo los recepcionistas pueden registrar ventas")
            salida.descripcion = "Solo los recepcionistas pueden registrar ventas"
            salida.estatus = "Error"
            return salida

        total_venta = 0
        detalles = []

        for item in venta_data.productos:
            producto = db.query(Producto).filter(Producto.idproductos == item.id_producto).first()
            if not producto:
                #raise HTTPException(status_code=404, detail=f"Producto ID {item.id_producto} no encontrado")
                salida.descripcion = f"Producto ID {item.id_producto} no encontrado"
                salida.estatus = "Error"
                return salida
            if producto.existencias < item.cantidad:
                #raise HTTPException(status_code=400, detail=f"Producto {producto.nombre} sin existencias suficientes")
                salida.descripcion = f"Producto {producto.nombre} sin existencias suficientes"
                salida.estatus = "Error"
                return salida

            subtotal = item.cantidad * producto.precio
            total_venta += subtotal
            detalles.append({
                "producto": producto,
                "cantidad": item.cantidad,
                "precio_unitario": producto.precio,
                "subtotal": subtotal
            })

        nueva_venta = Venta(
            id_usuario=venta_data.id_usuario,
            fecha=venta_data.fecha,
            total=total_venta,
            comentarios=venta_data.comentarios
        )
        db.add(nueva_venta)
        db.commit()
        db.refresh(nueva_venta)

        for d in detalles:
            producto = d["producto"]
            producto.existencias -= d["cantidad"]
            detalle = DetalleVenta(
                id_venta=nueva_venta.idVenta,
                id_producto=producto.idproductos,
                cantidad=d["cantidad"],
                precio_unitario=d["precio_unitario"],
                subtotal=d["subtotal"]
            )
            db.add(detalle)

        db.commit()
        salida.descripcion = "Venta creada exitosamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = "La creación de la venta ha fallado"
        salida.estatus = "Fallido"
    return salida

def actualizar_comentarios_venta(db: Session, id_venta: int, nuevos_comentarios: str):
    salida = Salida(descripcion="", estatus="")
    try:
        venta = db.query(Venta).filter(Venta.idVenta == id_venta).first()
        if not venta:
            salida.descripcion = f"No se encontró la venta {id_venta}"
            salida.estatus = "Fallido"
            return salida
        venta.comentarios = nuevos_comentarios
        db.commit()
        db.refresh(venta)
        salida.descripcion = f"Venta modificada con éxito"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = "La creación de la venta ha fallado"
        salida.estatus = "Fallido"
    return salida

def obtener_ventas_por_rango(db: Session, fecha_inicio: date, fecha_fin: date) -> List[Venta]:
    return db.query(Venta).options(
        joinedload(Venta.detalles).joinedload(DetalleVenta.producto)
    ).filter(
        Venta.fecha >= fecha_inicio,
        Venta.fecha <= fecha_fin
    ).all()