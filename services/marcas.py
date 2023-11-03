from datetime import datetime
from typing import List
from bson import ObjectId
from db_mongo.conexion_mongo import db_cliente as db
from schemas.marcas import Marcas
from db_mongo.models.marcas import Marcas_DB

def obtener_marca_db(campo: str, valor) -> Marcas:
    try: 
        marca_db = db.local.marcas.find_one(
            { campo: valor })
        if marca_db["estado"] >= 1:
            return marca_schema(marca_db)
        else:
            return ""
    except ConnectionError as e:
       return str(e)
    
def obtener_marcas_db() -> List[Marcas]:
    try: 
        resultado_db = db.local.marcas.find(
            { "estado": 1 })
        marcas_db = list(resultado_db)
        if len(marcas_db) >= 1:
            return marcas_schema(marcas_db)
        else:
            return ""
    except ConnectionError as e:
       return str(e)
    
def insertar_marca_db(marca: Marcas, fecha_insercion: datetime) ->Marcas:

    marca_existente = db.local.marcas.find_one({"descrip_marca": marca.descrip_marca})
    if type(marca_existente) == Marcas:
        if marca_existente["estado"] == 1:
            return "La marca ya existe"
        elif marca_existente["estado"] == 0:
            filtro = { '_id': ObjectId(marca_existente["_id"]) }
            nuevos_valores = { 
                "$set": { 
                'fecha_insercion': fecha_insercion,
                'estado': 1
                } 
                }
            editado = db.local.marcas.find_one_and_update(filtro, nuevos_valores)
            return marca_schema(editado)
    else:
        marca_dict = dict(marca_models(marca, fecha_insercion))
        del marca_dict["id"]
        print("creo")
        try:
            id = db.local.marcas.insert_one(marca_dict).inserted_id
            marca_devuelta: Marcas = obtener_marca_db("_id", id)
            return marca_devuelta
        except ConnectionError as e:
            return str(e)

def editar_marca_db(marca: Marcas, fecha_insercion: datetime) ->Marcas:

    filtro = { '_id': ObjectId(marca.id) }
    nuevos_valores = { 
        "$set": { 
        'descrip_marca': marca.descrip_marca,
        'fecha_insercion': fecha_insercion
        } 
        }   
    marca_existente = db.local.marcas.find_one({"descrip_marca": marca.descrip_marca})
    if type(marca_existente) == dict:
        if marca_existente["estado"] == 1:
            return "La marca ya existe"
    else:
        try:
            editado = db.local.marcas.find_one_and_update(filtro, nuevos_valores)
            return marca_schema(editado)
        except ConnectionError as e:
            return str(e)
    
def eliminar_marca_db(campo: str, valor, fecha_insercion: datetime) ->Marcas:

    filtro = { campo: ObjectId(valor) }
    nuevos_valores = { 
        "$set": { 
        'fecha_insercion': fecha_insercion,
        'estado': 0
        } 
        }
    
    try:
        editado = db.local.marcas.find_one_and_update(filtro, nuevos_valores)
        return marca_schema(editado)
    except ConnectionError as e:
            return str(e)

def marca_schema(marca_db: dict) ->Marcas:   
    marca: dict = {
        "id": str(marca_db["_id"]),
        "descrip_marca": marca_db["descrip_marca"],
    }
    return Marcas(**marca)

def marcas_schema(marca_db: List) ->List[Marcas]: 
    
    marcas: List = [marca_schema(marca) for marca in marca_db]  
    return marcas

def marca_models(marca_db: Marcas, fecha_insercion: datetime) ->Marcas_DB:    
    marca: dict ={
        "id": marca_db.id,
        "descrip_marca": marca_db.descrip_marca.upper(),
        "fecha_insercion": fecha_insercion,
        "estado": 1
    }
    return Marcas_DB(**marca)