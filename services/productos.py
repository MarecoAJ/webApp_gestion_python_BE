from typing import List
from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from db.db_mongo.services_db.productos import editar_producto_db, eliminar_producto_db, insertar_producto_db, obtener_producto_db, obtener_productos_db

from db.models.productos import Productos_DB
from schemas.productos import Productos

EXC_NO_ENCONTRADO = HTTPException(
    status_code= status.HTTP_404_NOT_FOUND,
    detail= "No se a encontrado el producto")

def obtener_producto_serv(campo: str, valor) ->Productos:
    producto_db = obtener_producto_db(campo, valor)
    producto = producto_schema(producto_db)
    if not producto:
        if producto == "":
            raise EXC_NO_ENCONTRADO
        else:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=producto)
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(producto))

def todos_productos_serv() ->List[Productos]:
    productos_db = obtener_productos_db()
    productos = productos_schema(productos_db)
    if not productos:
        if productos == "":
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "No se han encontrado productos")
        else:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=productos)
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(productos))

def insertar_producto_serv(datos: Productos) ->Productos:

    productos_devuelta = insertar_producto_db(datos)
    if type(productos_devuelta) == str:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= productos_devuelta)
    else:
        producto = producto_schema(productos_devuelta)

    return JSONResponse(status_code= status.HTTP_201_CREATED, content= jsonable_encoder(producto))

def editar_producto_serv(producto: Productos) ->Productos:

    producto_editado = editar_producto_db(producto)
    if type(producto_editado) == str:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=producto_editado)
    else:
        producto = producto_schema(producto_editado)
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(producto))

def eliminar_producto_serv(id) ->Productos:

    producto_borrado = eliminar_producto_db("_id", ObjectId(id))
    if type(producto_borrado) == str:
        raise EXC_NO_ENCONTRADO
    else:
        producto = producto_schema(producto_borrado)
    
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(producto))

def producto_schema(producto_db: Productos_DB) ->Productos:
    producto = dict(
        {
            "id": producto_db.id,
            "descrip_produc": producto_db.descrip_produc,
            "modelo_id": producto_db.modelo_id,
            "cant_produc": producto_db.cant_produc,
            "min_cant_produc": producto_db.min_cant_produc
        }
    )
    return Productos(**producto)

def productos_schema(producto_db: List[Productos_DB]) ->List[Productos]:
    productos: List = [producto_schema(producto_db) for producto in producto_db]
    return productos
