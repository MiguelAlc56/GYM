from sqlalchemy.orm import Session
from schema.PersonaSchema import Persona
from schema.EmpleadosSchema import Empleado
from models.EmpleadosModel import empleadoInsert, Salida, EmpleadoUpdate
from datetime import datetime
from typing import List

def insertar_empleado(db: Session, cliente_data: empleadoInsert):
    salida = Salida(descripcion="", estatus="")
    try:
        # 1. Insertar en persona
        persona = Persona(
            Nombre=cliente_data.Nombre,
            Apellido=cliente_data.Apellido,
            FechaNacimineto=cliente_data.FechaNacimineto,
            Telefono=cliente_data.Telefono,
            Correo=cliente_data.Correo,
            Sexo=cliente_data.Sexo
        )
        db.add(persona)
        db.commit()
        db.refresh(persona)

        # 2. Insertar en cliente
        empleado = Empleado(
            Contraseña=cliente_data.Contraseña,
            Roll=cliente_data.Roll,
            Estatus=cliente_data.Estatus,
            id_persona=persona.idPersona
        )
        db.add(empleado)
        db.commit()
        db.refresh(empleado)
        salida.descripcion = f"El Empelado {empleado.idEmpleados} insertado correctamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = f"No se pudo agregar al Empleado "
        salida.estatus = "Fallido"
    return salida

def obtener_empleado_por_id(db: Session, id_empleado: int):
    return db.query(Empleado).filter(Empleado.idEmpleados == id_empleado).first()

def obtener_todos_los_empleados(db: Session) -> List[Empleado]:
    return db.query(Empleado).all()

def actualizar_empleado(db: Session, id_empleado: int, empleado_data: EmpleadoUpdate):
    salida = Salida(descripcion="", estatus="")
    try:
        empleado = db.query(Empleado).filter(Empleado.idEmpleados == id_empleado).first()
        if not empleado:
            salida.descripcion = f"No se encontró ningún empleado con el id {id_empleado}"
            salida.estatus = "Fallido"
            return salida

        # Actualizar datos de persona
        persona = empleado.persona
        if empleado_data.Nombre is not None:
            persona.Nombre = empleado_data.Nombre
        if empleado_data.Apellido is not None:
            persona.Apellido = empleado_data.Apellido
        if empleado_data.FechaNacimineto is not None:
            persona.FechaNacimineto = empleado_data.FechaNacimineto
        if empleado_data.Telefono is not None:
            persona.Telefono = empleado_data.Telefono
        if empleado_data.Correo is not None:
            persona.Correo = empleado_data.Correo
        if empleado_data.Sexo is not None:
            persona.Sexo = empleado_data.Sexo

        # Actualizar datos de cliente
        if empleado_data.Contraseña is not None:
            empleado.Contraseña = empleado_data.Contraseña
        if empleado_data.Roll  is not None:
            empleado.Roll = empleado_data.Roll
        if empleado_data.Estatus is not None:
            empleado.Estatus = empleado_data.Estatus

        db.commit()
        db.refresh(empleado)
        salida.descripcion = f"El empleado con el id {empleado.idEmpleados} ha sido actualizado correctamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = f"El empleado {id_empleado} no ha podido ser actualizado"
        salida.estatus = "Fallido"
    return salida

def eliminar_empleado(db: Session, id_empleado: int):
    salida = Salida(descripcion="", estatus="")
    try:
        empleado = db.query(Empleado).filter(Empleado.idEmpleados == id_empleado).first()
        if not empleado:
            salida.descripcion = f"No se encontró ningún empleado con el id {id_empleado}"
            salida.estatus = "Fallido"
            return salida

        persona = empleado.persona

        db.delete(empleado)
        db.delete(persona)
        db.commit()
        salida.descripcion = f"El empleado {empleado.idEmpleados} eliminado correctamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = f"El empleado {id_empleado} no ha podido ser eliminado"
        salida.estatus = "Fallido"
    return salida
