from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from services.usuarios import validar_usuario

usuarios_router = APIRouter(prefix="/usuarios",
                   tags=["Usuarios"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@usuarios_router.post("/inicio_sesion")
async def inicio_sesion(form: OAuth2PasswordRequestForm = Depends()):
    
    token = validar_usuario(form.username, form.password)
    return token