from datetime import datetime
from typing import List 
from db.models.modelos import Modelos_DB
from schemas.modelos import Modelos
from db.db_mongo.conexion_mongo import db_cliente as db
from bson import ObjectId

fecha_insercion: datetime = datetime

def obtener_modelos_db() -> List[Modelos_DB]:
    try:    
        resultado_db = db.web_gestion.modelos.find(
            { "estado": 1 })
        modelos_db = list(resultado_db)
        if len(modelos_db) >= 1:
            return modelo_model(modelos_db)
    except ConnectionError as e:
        return str(e) 

def obtener_modelo_db(campo: str, valor) ->Modelos_DB:
    try:
        resultado_db = db.web_gestion.modelos.find_one({"$and": [{campo: valor}, {"estado": 1}]})
        modelo_db = modelo_model(resultado_db)
        if not modelo_db:
            return ""
        else:
            return modelo_db
    except ConnectionError as e:
        return str(e) 
  
def editar_modelo_db(modelo: Modelos) ->Modelos_DB:
    try:
        filtro = { '_id': ObjectId(modelo.id)}
        nuevos_valores = {
           "$set": {
               'descrip_modelo': modelo.descrip_modelo,
               'marca_id': ObjectId(modelo.marca_id),
               'fecha_insercion': fecha_insercion,
           }
        }
        modelo_existente = db.web_gestion.modelos.find_one_and_update(filtro, nuevos_valores)
        if type(modelo_existente) == dict:
            if modelo_existente["estado"] == 1:
                return "El modelo ya existe"
        else:
            editado = db.web_gestion.modelos.find_one_and_update(filtro, nuevos_valores)
            return modelo_model(editado)
    except ConnectionError as e:
        return str(e)

def insertar_modelo_db(modelo: Modelos) ->Modelos_DB:

    try:
        modelo_existente = db.web_gestion.modelos.find_one({"descrip_modelo": modelo.descrip_modelo.upper()})
        if type(modelo_existente) == dict:
            return "El modelo ya existe"
        elif modelo_existente["estado"] == 0:
            filtro = { '_id': ObjectId(modelo_existente["id"]) }
            nuevos_valores = {
                "$set": {
                    'fecha_insercion': fecha_insercion,
                    'estado': 1
                }
            }
            editado = db.web_gestion.modelos.find_one_and_update(filtro, nuevos_valores)
            return modelo_model(editado)
        else:
            modelo_dict = dict(crear_modelo_db(modelo))
            del modelo_dict["id"]
            id = db.web_gestion.modelos.insert_one(modelo_dict).inserted_id
            modelo_devuelta: Modelos = obtener_modelo_db("_id", id)
            return modelo_devuelta
        
    except ConnectionError as e:
        return str(e)

def eliminar_modelo_db(campo: str, valor) ->Modelos_DB:
    try:
        filtro = { campo: ObjectId(valor)}
        nuevos_valores = {
            "$set": {
                'fecha_insercion': fecha_insercion,
                'estado': 0
            }
        }
        editado = db.web_gestion.modelos.find_one_and_update(filtro, nuevos_valores)
        if type(editado) == dict:
            return modelo_model(editado)
        else:
            return ""
    except ConnectionError as e:
        return str(e)    

def modelo_model(modelo_db: dict) ->Modelos_DB:
    modelo = {
        "id": str(modelo_db["_id"]),
        "descrip_modelo": modelo_db["descrip_modelo"],
        "marca_id": str(modelo_db["marca_id"]),
        "fecha_insercion": modelo_db["fecha_insercion"],
        "estado": modelo_db["estado"]
    }
    return Modelos_DB(**modelo)

def modelos_model(modelos: List) -> List[Modelos_DB]:
    
    modelos: list = [modelo_model(modelo) for modelo in modelos]
    return modelos

def crear_modelo_db(modelo: Modelos) ->Modelos_DB:
    modelo_db: dict = {
        "id": modelo.id,
        "descrip_modelo": modelo.descrip_modelo,
        "marca_id": modelo.marca_id,
        "fecha_insercion": fecha_insercion,
        "estado": 1
    }
    return Modelos_DB(**modelo_db)