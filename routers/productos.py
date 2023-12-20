
from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, status
from middlewares.jwt_usuarios import validar_admin
from schemas.productos import Productos
from services.productos import editar_producto_serv, eliminar_producto_serv, insertar_producto_serv, obtener_producto_serv, todos_productos_serv
from services.usuarios import validar_autentificacion


productos_router = APIRouter(prefix="/productos", tags=["Productos"])

@productos_router.get("/{id}", response_model= Productos, status_code= status.HTTP_200_OK)
async def obtener_producto(id: str, ok: bool = Depends(validar_autentificacion)) ->Productos:
    if ok:
        producto = obtener_producto_serv('_id', ObjectId(id))
        return producto
    
@productos_router.get("/", response_model= List[Productos], status_code= status.HTTP_200_OK)
async def obtener_productos(ok: bool = Depends(validar_autentificacion)) ->Productos:
    if ok:
        productos = todos_productos_serv()
        return productos
    
@productos_router.post("/", response_model= Productos, status_code= status.HTTP_201_CREATED)
async def insertar_producto(datos: Productos, ok: bool = Depends(validar_admin)) ->Productos:
    if ok:
        producto_devuelto = insertar_producto_serv(datos)
        return producto_devuelto
    
@productos_router.put("/", response_model= Productos, status_code= status.HTTP_200_OK)
async def actualizar_producto(producto: Productos, ok: bool = Depends(validar_admin)) ->Productos:
    if ok:
        producto_editado = editar_producto_serv(producto)
        return producto_editado
    
@productos_router.delete("/{id}", response_model= Productos, status_code= status.HTTP_200_OK)
async def eliminar_producto(id: str, ok: bool = Depends(validar_admin)) ->Productos:
    if ok:
        producto_borrado = eliminar_producto_serv(id)
        return producto_borrado