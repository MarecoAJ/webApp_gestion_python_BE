from typing import List
from datetime import datetime

from bson import ObjectId
from db.models.productos import Productos_DB
from schemas.productos import Productos
from db.db_mongo.conexion_mongo import db_cliente as db

fecha_insercion: datetime = datetime

def obtener_productos_db() -> List[Productos_DB]:
    try:
        resultado_db = db.web_gestion.productos.find(
            {"estado": 1})
        productos_db = list(resultado_db)
        if len(productos_db) >= 1:
            return productos_model(productos_db)
    except ConnectionError as e:
        return str(e)

def obtener_producto_db(campo: str, valor) ->Productos_DB:
    try:
        resultado_db = db.web_gestion.productos.find_one({"$and": [{campo: valor}, {"estado": 1}]})
        producto_db = producto_model(resultado_db)
        if not producto_model:
            return ""
        else:
            return producto_db
    except ConnectionError as e:
        return str(e)

def editar_producto_db(producto: Productos) -> Productos_DB:
    try:
        filtro = {'_id': ObjectId(producto.id)}
        nuevos_valores = {
            "$set": {
                'descrip_produc': producto.descrip_produc,
                'modelo_id': ObjectId(producto.modelo_id),
                'cant_produc': producto.cant_produc,
                'min_cant_produc': producto.min_cant_produc,
                'fecha_insercion': fecha_insercion,
            }
        }
        producto_existente = db.web_gestion.productos.find_one_and_update(filtro, nuevos_valores)
        if type(producto_existente) == dict:
            if producto_existente["estado"] == 1:
                return "El producto ya existe"
        else:
            editado = db.web_gestion.productos.find_one_and_update(filtro, nuevos_valores)
            return producto_model(editado)
    except ConnectionError as e:
        return str(e)

def insertar_producto_db(producto: Productos) ->Productos_DB:
    try:
        producto_existente = db.web_gestion.productos.find_one({"descrip_produc": producto.descrip_produc.upper()})
        if type(producto_existente) == dict:
            return "El producto ya existe"
        elif producto_existente["estado"] == 0:
            filtro = {'_id': ObjectId(producto_existente["id"])}
            nuevos_valores = {
                "$set": {
                    'fecha_insercion': fecha_insercion,
                    'estado': 1
                }
            }
            editado = db.web_gestion.productos.find_one_and_update(filtro, nuevos_valores)
            return producto_model(editado)
        else:
            producto_dict = dict(crear_producto_db(producto))
            del producto_dict["id"]
            id = db.web_gestion.productos.insert_one(producto_dict).inserted_id
            producto_devuelta: Productos = obtener_modelo_db("_id", id)
            return producto_devuelta
        
    except ConnectionError as e:
        return str(e)

def eliminar_producto_db(campo: str, valor) ->Productos_DB:
    try:
        filtro = { campo: ObjectId(valor)}
        nuevos_valores = {
            "$set": {
                'fecha_insercion': fecha_insercion,
                'estado': 0
            }
        }
        editado = db.web_gestion.productos.find_one_and_delete(filtro, nuevos_valores)
        if type(editado) == dict:
            return producto_model(editado)
        else:
            return ""
    except ConnectionError as e:
        return str(e)

def producto_model(producto_db: dict) -> Productos_DB:
    producto = {
        "id": str(producto_db["_id"]),
        "descrip_produc": producto_db["descrip_produc"],
        "modelo_id": str(producto_db["modelo_id"]),
        "cant_produc": producto_db["cant_produc"],
        "min_cant_produc": producto_db["min_cant_produc"],
        "fecha_insercion": producto_db["fecha_insercion"],
        "estado": producto_db["estado"]
    }
    return Productos_DB(**producto)

def productos_model(productos: List) -> List[Productos_DB]:

    productos: list = [producto_model(producto) for producto in productos]
    return productos

def crear_producto_db(producto: Productos) ->Productos_DB:
    producto_db: dict = {
        "id": producto.id,
        "descrip_produc": producto.descrip_produc,
        "modelo_id": producto.modelo_id,
        "cant_produc": producto.cant_produc,
        "min_cant_produc": producto.min_cant_produc,
        "fecha_insercion": fecha_insercion,
        "estado": 1
    }
    return Productos_DB(**producto_db)