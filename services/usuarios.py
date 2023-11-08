from fastapi import Depends, HTTPException,status
from db.db_mongo.services_db.usuarios import obtener_usuario_db
from db.models.usuarios import Usuario_DB
from middlewares.jwt_usuarios import crear_access_token, crear_token, desencriptar, validar_admin
from schemas.usuarios import Usuario

def validar_usuario(username: str, password: str) ->dict:
    
    usuario_db = obtener_usuario_db("nombre_usuario", username)
    usuario = usuario_schema(usuario_db)
    if usuario == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail= "El usuario no es correcto")

    if not desencriptar( password, usuario.contrasennia_usuario):

       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail= "La contraseña no es correcta") 
    
    acceso = crear_access_token(usuario.nombre_usuario)
    token = crear_token(acceso)
    
    return token

def validar_autorizacion(ok: bool = Depends(validar_admin)) ->bool:
    if not ok:
       raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})
    
    return ok

def usuario_schema(usuario_db: Usuario_DB) -> Usuario:

    usuario = dict(
            {
                "nombre_usuario": usuario_db.nombre_usuario,
                "contrasennia_usuario": usuario_db.contrasennia_usuario,
                "tipo": usuario_db.tipo
            }
        )
    return Usuario(**usuario)