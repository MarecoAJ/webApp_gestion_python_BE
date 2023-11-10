from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, status
from middlewares.jwt_usuarios import validar_admin
from schemas.marcas import Marcas
from services.marcas import editar_marca_serv, eliminar_marca_serv, insertar_marca_serv, obtener_marca_serv, todas_marcas_serv
from services.usuarios import validar_autentificacion

marcas_router = APIRouter(prefix="/marcas", tags=["Marcas"])

@marcas_router.get("/{id}", response_model= Marcas, status_code= status.HTTP_200_OK)
async def obtener_marca(id: str, ok: bool = Depends(validar_autentificacion)) -> Marcas:
    if ok:
        marca = obtener_marca_serv('_id', ObjectId(id))
        return marca

@marcas_router.get("/", response_model= List[Marcas], status_code= status.HTTP_200_OK)
async def obtener_marcas(ok: bool = Depends(validar_autentificacion)) -> List[Marcas]:
    if ok:
        marcas = todas_marcas_serv()    
        return marcas

@marcas_router.post("/", response_model= Marcas, status_code= status.HTTP_201_CREATED)
async def insertar_marca(datos: Marcas, ok: bool = Depends(validar_admin)) -> Marcas:
    if ok:
        marca_devuelta = insertar_marca_serv(datos) 
        return marca_devuelta

@marcas_router.put("/", response_model= Marcas, status_code= status.HTTP_200_OK)
async def actualizar_marca(marca: Marcas, ok: bool = Depends(validar_admin)) -> Marcas:
    if ok:
        marca_editada = editar_marca_serv(marca)
        return marca_editada

@marcas_router.delete("/{id}", response_model=Marcas, status_code=status.HTTP_200_OK)
async def eliminar_marca(id: str, ok: bool = Depends(validar_admin)) -> Marcas:
    if ok:
        marca_borrada = eliminar_marca_serv(id)
        return marca_borrada
