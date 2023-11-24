from fastapi import HTTPException, status
from typing import List
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from db.db_mongo.services_db.marcas import editar_marca_db, insertar_marca_db, obtener_marcas_db, obtener_marca_db, eliminar_marca_db
from schemas.marcas import Marcas
from db.models.marcas import Marcas_DB

EXC_NO_ENCONTRADO = HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= "No se a encontrado la marca")

def obtener_marca_serv(campo: str, valor) -> Marcas:
    marca_db = obtener_marca_db(campo, valor)
    marca = marca_schema(marca_db)
    if not marca:
        if marca == "":
            raise EXC_NO_ENCONTRADO
        else:
            raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail= marca)   
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(marca))
    
def todas_marcas_serv() -> List[Marcas]: 
    marcas_db = obtener_marcas_db()
    marcas = marcas_schema(marcas_db)
    if not marcas:
        if marcas == "":
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail= "No se han encontrado marcas")
        else:
            raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail= marcas)
        
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(marcas))
    
def insertar_marca_serv(datos: Marcas) ->Marcas:
    
    marca_devuelta = insertar_marca_db(datos)
    if type(marca_devuelta) == str:
        raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail= marca_devuelta)
    else:
        marca = marca_schema(marca_devuelta)

    return JSONResponse(status_code= status.HTTP_201_CREATED, content= jsonable_encoder(marca))

def editar_marca_serv(marca: Marcas) ->Marcas:

    marca_editada = editar_marca_db(marca)
    if type(marca_editada) == str:
        raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail= marca_editada)
    else:
        marca = marca_schema(marca_editada)
    
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(marca))
    
def eliminar_marca_serv(id) ->Marcas:
    
    marca_borrada = eliminar_marca_db("_id", ObjectId(id))
    if type(marca_borrada) == str:
        raise EXC_NO_ENCONTRADO
    else:
        marca = marca_schema(marca_borrada)

    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(marca))

def marca_schema(marca_db: Marcas_DB) ->Marcas: 
    marca = dict(
        {
            "id": marca_db.id,
            "descrip_marca": marca_db.descrip_marca
        }
    )
    return Marcas(**marca)

def marcas_schema(marca_db: List[Marcas_DB]) ->List[Marcas]: 
    marcas: List = [marca_schema(marca) for marca in marca_db]  
    return marcas