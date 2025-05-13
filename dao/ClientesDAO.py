from sqlalchemy.orm import Session
from schema.PersonaSchema import Persona
from schema.ClientesSchema import Cliente
from models.ClientesModel import clienteInsert, Salida, ClienteUpdate
from datetime import datetime
from typing import List

def insertar_cliente(db: Session, cliente_data: clienteInsert):
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
        cliente = Cliente(
            Fecha_Adquisicion=cliente_data.Fecha_Adquisicion,
            Estatus=cliente_data.Estatus,
            id_persona=persona.idPersona
        )
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        salida.descripcion = f"Cliente {cliente.idClientes} insertado correctamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = f"Fallo en la agregación del cliente"
        salida.estatus = "Fallido"
    return salida

def obtener_cliente_por_id(db: Session, id_cliente: int):
    return db.query(Cliente).filter(Cliente.idClientes == id_cliente).first()

def obtener_todos_los_clientes(db: Session) -> List[Cliente]:
    return db.query(Cliente).all()

def actualizar_cliente(db: Session, id_cliente: int, cliente_data: ClienteUpdate):
    salida = Salida(descripcion="", estatus="")
    try:
        cliente = db.query(Cliente).filter(Cliente.idClientes == id_cliente).first()
        if not cliente:
            salida.descripcion = f"No se encontró ningún cliente con el id {id_cliente}"
            salida.estatus = "Fallido"
            return salida

        # Actualizar datos de persona
        persona = cliente.persona
        if cliente_data.Nombre is not None:
            persona.Nombre = cliente_data.Nombre
        if cliente_data.Apellido is not None:
            persona.Apellido = cliente_data.Apellido
        if cliente_data.FechaNacimineto is not None:
            persona.FechaNacimineto = cliente_data.FechaNacimineto
        if cliente_data.Telefono is not None:
            persona.Telefono = cliente_data.Telefono
        if cliente_data.Correo is not None:
            persona.Correo = cliente_data.Correo
        if cliente_data.Sexo is not None:
            persona.Sexo = cliente_data.Sexo

        # Actualizar datos de cliente
        if cliente_data.Fecha_Adquisicion is not None:
            cliente.Fecha_Adquisicion = cliente_data.Fecha_Adquisicion
        if cliente_data.Estatus is not None:
            cliente.Estatus = cliente_data.Estatus

        db.commit()
        db.refresh(cliente)
        salida.descripcion = f"El cliente con el id {cliente.idClientes} ha sido actualizado correctamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = f"El cliente {id_cliente} no ha podido ser actualizado"
        salida.estatus = "Fallido"
    return salida

def eliminar_cliente(db: Session, id_cliente: int):
    salida = Salida(descripcion="", estatus="")
    try:
        cliente = db.query(Cliente).filter(Cliente.idClientes == id_cliente).first()
        if not cliente:
            salida.descripcion = f"No se encontró ningún cliente con el id {id_cliente}"
            salida.estatus = "Fallido"
            return salida

        persona = cliente.persona

        db.delete(cliente)
        db.delete(persona)
        db.commit()
        salida.descripcion = f"Cliente {cliente.idClientes} eliminado correctamente"
        salida.estatus = "OK"
    except Exception as ex:
        print(ex)
        salida.descripcion = f"El cliente {id_cliente} no ha podido ser eliminado"
        salida.estatus = "Fallido"    
    return Salida