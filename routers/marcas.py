from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schemas.marcas import Marcas
from datetime import datetime
from services.marcas import insertar_marca_db, obtener_marca_db, editar_marca_db, eliminar_marca_db, obtener_marcas_db

marcas_router = APIRouter(prefix="/marcas", tags=["Marcas"])

fecha_insercion: datetime = datetime.now() 

EXC_NO_ENCONTRADO = HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= "No se a encontrado la marca")

@marcas_router.get("/{id}", response_model= Marcas, status_code= status.HTTP_200_OK)
async def obtener_marca(id: str) -> Marcas:

    marca = obtener_marca_db( "_id", ObjectId(id) )
    if not marca:
        if marca == "":
            raise EXC_NO_ENCONTRADO
        else:
            raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail= marca)   
        
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(marca))

@marcas_router.get("/", response_model= List[Marcas], status_code= status.HTTP_200_OK)
async def obtener_marcas() -> List[Marcas]:

    marcas = obtener_marcas_db()
    if not marcas:
        if marcas == "":
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail= "No se han encontrado marcas")
        else:
            raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail= marcas)
        
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(marcas))

@marcas_router.post("/", response_model= Marcas, status_code= status.HTTP_201_CREATED)
async def insertar_marca(marca: Marcas) -> Marcas:

    marca_devuelta = insertar_marca_db(marca, fecha_insercion)
    if not marca_devuelta:
        raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail= marca_devuelta)
    
    return JSONResponse(status_code= status.HTTP_201_CREATED, content= jsonable_encoder(marca_devuelta))

@marcas_router.put("/", response_model= Marcas, status_code= status.HTTP_200_OK)
async def actualizar_marca(marca: Marcas) -> Marcas:

    marca_editada = editar_marca_db(marca, fecha_insercion)
    if not marca_editada:
        raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail= marca_editada)
    
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(marca_editada))

@marcas_router.delete("/{id}", response_model=Marcas, status_code=status.HTTP_200_OK)
async def eliminar_marca(id: str) -> Marcas:
    
    marca_borrada = eliminar_marca_db("_id", ObjectId(id), fecha_insercion)
    if not marca_borrada:
        raise EXC_NO_ENCONTRADO
    return JSONResponse(status_code= status.HTTP_200_OK, content= jsonable_encoder(marca_borrada))
