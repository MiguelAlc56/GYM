from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from models.MembresiaModel import Salida, MembresiaInsert, MembresiaUpdate, AsignacionMembresia
from schema.MembresiaSchema import Membresia
from schema.DetalleMembresiaSchema import DetalleMembresia
from schema.ClientesSchema import Cliente
from schema.EmpleadosSchema import Empleado


def insertar_membresia(db: Session, membresia_data: MembresiaInsert) -> Salida:
    salida = Salida(descripcion="", estatus="")
    try:
        nueva_membresia = Membresia(
            Nombre=membresia_data.Nombre,
            Descripcion=membresia_data.Descripcion,
            Precio=membresia_data.Precio,
            Vigencia=membresia_data.Vigencia
        )
        db.add(nueva_membresia)
        db.commit()
        db.refresh(nueva_membresia)
        salida.descripcion = f"La membresía {nueva_membresia.idMembresias} insertada correctamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = "No se pudo agregar la membresía"
        salida.estatus = "Fallido"
        db.rollback()
    return salida


def obtener_membresia_por_id(db: Session, id_membresia: int):
    return db.query(Membresia).filter(Membresia.idMembresias == id_membresia).first()


def obtener_todas_las_membresias(db: Session) -> List[Membresia]:
    return db.query(Membresia).all()


def actualizar_membresia(db: Session, id_membresia: int, membresia_data: MembresiaUpdate) -> Salida:
    salida = Salida(descripcion="", estatus="")
    try:
        membresia = db.query(Membresia).filter(Membresia.idMembresias == id_membresia).first()
        if not membresia:
            salida.descripcion = f"No se encontró ninguna membresía con el id {id_membresia}"
            salida.estatus = "Fallido"
            return salida

        if membresia_data.Nombre is not None:
            membresia.Nombre = membresia_data.Nombre
        if membresia_data.Descripcion is not None:
            membresia.Descripcion = membresia_data.Descripcion
        if membresia_data.Precio is not None:
            membresia.Precio = membresia_data.Precio
        if membresia_data.Vigencia is not None:
            membresia.Vigencia = membresia_data.Vigencia

        db.commit()
        db.refresh(membresia)
        salida.descripcion = f"La membresía con el id {membresia.idMembresias} ha sido actualizada correctamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = f"La membresía {id_membresia} no ha podido ser actualizada"
        salida.estatus = "Fallido"
        db.rollback()
    return salida


def eliminar_membresia(db: Session, id_membresia: int) -> Salida:
    salida = Salida(descripcion="", estatus="")
    try:
        membresia = db.query(Membresia).filter(Membresia.idMembresias == id_membresia).first()
        if not membresia:
            salida.descripcion = f"No se encontró ninguna membresía con el id {id_membresia}"
            salida.estatus = "Fallido"
            return salida

        # Verificar si la membresía está asignada a algún cliente
        asignaciones = db.query(DetalleMembresia).filter(
            DetalleMembresia.id_membresia == id_membresia
        ).count()

        if asignaciones > 0:
            salida.descripcion = "No se puede eliminar, la membresía está asignada a clientes"
            salida.estatus = "Fallido"
            return salida

        db.delete(membresia)
        db.commit()
        salida.descripcion = f"La membresía {id_membresia} eliminada correctamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = f"La membresía {id_membresia} no ha podido ser eliminada"
        salida.estatus = "Fallido"
        db.rollback()
    return salida


def asignar_membresia_cliente(db: Session, asignacion_data: AsignacionMembresia) -> Salida:
    salida = Salida(descripcion="", estatus="")
    try:
        # Verificar que el cliente existe
        cliente = db.query(Cliente).filter(Cliente.idClientes == asignacion_data.id_cliente).first()
        if not cliente:
            salida.descripcion = "Cliente no encontrado"
            salida.estatus = "Fallido"
            return salida

        # Verificar que la membresía existe
        membresia = db.query(Membresia).filter(Membresia.idMembresias == asignacion_data.id_membresia).first()
        if not membresia:
            salida.descripcion = "Membresía no encontrada"
            salida.estatus = "Fallido"
            return salida

        # Verificar que el empleado existe
        empleado = db.query(Empleado).filter(Empleado.idEmpleados == asignacion_data.id_empleado).first()
        if not empleado:
            salida.descripcion = "Empleado no encontrado"
            salida.estatus = "Fallido"
            return salida

        # Verificar si el cliente ya tiene una membresía activa del mismo tipo
        membresia_activa = db.query(DetalleMembresia).filter(
            DetalleMembresia.id_cliente == asignacion_data.id_cliente,
            DetalleMembresia.id_membresia == asignacion_data.id_membresia,
            DetalleMembresia.Estatus == True
        ).first()

        if membresia_activa:
            salida.descripcion = "El cliente ya tiene esta membresía activa"
            salida.estatus = "Fallido"
            return salida

        # Calcular fecha de fin basada en la vigencia de la membresía
        fecha_fin = asignacion_data.FechaInicio + timedelta(days=membresia.Vigencia)

        nueva_asignacion = DetalleMembresia(
            FechaInicio=asignacion_data.FechaInicio,
            FechaFin=fecha_fin,
            Estatus=asignacion_data.Estatus,
            id_cliente=asignacion_data.id_cliente,
            id_membresia=asignacion_data.id_membresia,
            id_empleado=asignacion_data.id_empleado
        )

        db.add(nueva_asignacion)
        db.commit()
        salida.descripcion = f"Membresía asignada exitosamente al cliente {cliente.idClientes}"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = "Error al asignar membresía"
        salida.estatus = "Fallido"
        db.rollback()
    return salida


def obtener_membresias_cliente(db: Session, id_cliente: int) -> List[DetalleMembresia]:
    return db.query(DetalleMembresia).filter(
        DetalleMembresia.id_cliente == id_cliente
    ).order_by(DetalleMembresia.FechaFin.desc()).all()