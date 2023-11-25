from fastapi import HTTPException, status
from typing import List 
from bson import ObjectId 
from fastapi.encoders import jsonable_encoder
from db.db_mongo.services_db.modelos import editar_modelo_db, eliminar_modelo_db, obtener_modelo_db, insertar_modelo_db, obtener_modelos_db
from db.models.modelos import Modelos_DB
from fastapi.responses import JSONResponse
from schemas.modelos import Modelos


EXC_NO_ENCONTRADO = HTTPException(
    status_code= status.HTTP_404_NOT_FOUND, 
    detail= "No se a encontrado el modelos")

def obtener_modelo_serv(campo: str, valor) ->Modelos:
    modelo_db = obtener_modelo_db(campo, valor)
    modelo = modelo_schema(modelo_db)
    if not modelo:
        if modelo == "":
            raise EXC_NO_ENCONTRADO
        else:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=modelo)
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(modelo))

def todos_modelos_serv() ->List[Modelos]:
    modelos_db = obtener_modelos_db()
    modelos = modelos_schema(modelos_db)
    if not modelos:
        if modelos == "":
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND, detail= "No se han encontado modelos")
        else:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,    
                detail=modelos)
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(modelos))  

def insertar_modelo_serv(datos: Modelos) ->Modelos:

    modelos_devuelta = insertar_modelo_db(datos)
    if type(modelos_devuelta) == str:
        raise HTTPException(
                        status_code= status.HTTP_404_NOT_FOUND,
                        detail= modelos_devuelta)
    else:
        modelo = modelo_schema(modelos_devuelta)

    return JSONResponse(status_code= status.HTTP_201_CREATED, content= jsonable_encoder(modelo))    

def editar_modelo_serv(modelo: Modelos) ->Modelos:

    modelo_editada = editar_modelo_db(modelo)
    if type(modelo_editada) == str:
        raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail=modelo_editada)
    else:
        modelo = modelo_schema(modelo_editada)

    return JSONResponse(status_code=status.HTTP_200_OK, content= jsonable_encoder(modelo))

def eliminar_modelo_serv(id) ->Modelos:

    modelo_borrado = eliminar_modelo_db("_id", ObjectId(id))
    if type(modelo_borrado) == str:
        raise EXC_NO_ENCONTRADO
    else:
        modelo = modelos_schema(modelo_borrado)

    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(modelo))    

def modelo_schema(modelo_db: Modelos_DB) ->Modelos:
    modelo = dict(
        {
            "id": modelo_db.id,
            "descrip_modelo": modelo_db.descrip_modelo,
            "marca_id": modelo_db.marca_id
        }
    )
    return Modelos(**modelo)

def modelos_schema(modelo_db: List[Modelos_DB]) ->List[Modelos]:
    modelos: List = [modelo_schema(modelo) for modelo in modelo_db]
    return modelos