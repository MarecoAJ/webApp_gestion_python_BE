from datetime import datetime
from typing import List
from bson import ObjectId
from db.models.marcas import Marcas_DB
from db.db_mongo.conexion_mongo import db_cliente as db
from schemas.marcas import Marcas

fecha_insercion: datetime = datetime.now() 

def obtener_marcas_db() -> List[Marcas_DB]:
    try: 
        resultado_db = db.web_gestion.marcas.find(
            { "estado": 1 })
        marcas_db = list(resultado_db)
        if len(marcas_db) >= 1:
            return marcas_model(marcas_db)
        else:
            return ""
    except ConnectionError as e:
       return str(e)
    
def obtener_marca_db(campo: str, valor) -> Marcas_DB:
    try: 
        resultado_db = db.web_gestion.marcas.find_one({"$and": [{campo: valor}, {"estado": 1}]})
        marca_db = marca_model(resultado_db)
        if not marca_db:
            return ""
        else:
            return marca_db
    except ConnectionError as e:
       return str(e)
    
def editar_marca_db(marca: Marcas) ->Marcas_DB:

    try:
        filtro = { '_id': ObjectId(marca.id) }
        nuevos_valores = { 
            "$set": { 
            'descrip_marca': marca.descrip_marca,
            'fecha_insercion': fecha_insercion
            } 
            }   
        marca_existente = db.web_gestion.marcas.find_one({"descrip_marca": marca.descrip_marca})
        if type(marca_existente) == dict:
            if marca_existente["estado"] == 1:
                return "La marca ya existe"
        else:
            editado = db.web_gestion.marcas.find_one_and_update(filtro, nuevos_valores)
            return marca_model(editado)
    except ConnectionError as e:
        return str(e)

def insertar_marca_db(marca: Marcas) ->Marcas_DB:

    try:
        marca_existente = db.web_gestion.marcas.find_one({"descrip_marca": marca.descrip_marca.upper()})
        if type(marca_existente) == dict:
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
                editado = db.web_gestion.marcas.find_one_and_update(filtro, nuevos_valores)
                return marca_model(editado)
        else:
            marca_dict = dict(crear_marca_db(marca))
            del marca_dict["id"]
            id = db.web_gestion.marcas.insert_one(marca_dict).inserted_id
            marca_devuelta: Marcas = obtener_marca_db("_id", id)
            return marca_devuelta
        
    except ConnectionError as e:
        return str(e)
    
def eliminar_marca_db(campo: str, valor) ->Marcas_DB:

    try:
        filtro = { campo: ObjectId(valor) }
        nuevos_valores = { 
            "$set": { 
            'fecha_insercion': fecha_insercion,
            'estado': 0
            } 
            }
   
        editado = db.web_gestion.marcas.find_one_and_update(filtro, nuevos_valores)
        if type(editado) == dict:
                return marca_model(editado)
        else:
            return ""
    except ConnectionError as e:
        return str(e)

def marca_model(marca_db: dict) ->Marcas_DB:   
    marca = {
        "id": str(marca_db["_id"]),
        "descrip_marca": marca_db["descrip_marca"],
        "fecha_insercion": marca_db["fecha_insercion"],
        "estado": marca_db["estado"]
    }
    return Marcas_DB(**marca)

def marcas_model(marcas: List) ->List[Marcas_DB]: 
    
    marcas: List = [marca_model(marca) for marca in marcas]  
    return marcas

def crear_marca_db(marca: Marcas) ->Marcas_DB:    
    marca_db: dict ={
        "id": marca.id,
        "descrip_marca": marca.descrip_marca.upper(),
        "fecha_insercion": fecha_insercion,
        "estado": 1
    }
    return Marcas_DB(**marca_db)