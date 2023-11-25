from fastapi import APIRouter, Depends, status
from typing import List
from middlewares.jwt_usuarios import validar_admin
from schemas.modelos import Modelos
from services.usuarios import validar_autentificacion
from services.modelos import editar_modelo_serv, eliminar_modelo_serv, insertar_modelo_serv, obtener_modelo_serv, todos_modelos_serv
from bson import ObjectId

modelos_router = APIRouter(prefix="/modelos", tags=["Modelos"])

@modelos_router.get("/{id}", response_model= Modelos, status_code= status.HTTP_200_OK)
async def obtener_modelo(id: str, ok: bool = Depends(validar_autentificacion)) ->Modelos:
    if ok:
        modelo = obtener_modelo_serv('_id', ObjectId(id))
        return modelo
    
@modelos_router.get("/", response_model= List[Modelos], status_code= status.HTTP_200_OK)
async def obtener_modelos(ok: bool = Depends(validar_autentificacion)) ->Modelos:
    if ok:
        modelos = todos_modelos_serv()
        return modelos
    
@modelos_router.post("/", response_model= Modelos, status_code= status.HTTP_201_CREATED)
async def insertar_modelo(datos: Modelos, ok: bool = Depends(validar_admin)) ->Modelos:
    if ok:
        modelo_devuelta = insertar_modelo_serv(datos)
        return modelo_devuelta

@modelos_router.put("/", response_model= Modelos, status_code= status.HTTP_200_OK)
async def actualizar_modelo(modelo: Modelos, ok: bool = Depends(validar_admin)) ->Modelos:
    if ok:
        modelo_editado = editar_modelo_serv(modelo)
        return modelo_editado 
    
@modelos_router.delete("/{id}", response_model= Modelos, status_code= status.HTTP_200_OK)
async def eliminar_modelo(id: str, ok: bool = Depends(validar_admin)) ->Modelos:
    if ok:
        modelo_borrado = eliminar_modelo_serv(id)
        return modelo_borrado