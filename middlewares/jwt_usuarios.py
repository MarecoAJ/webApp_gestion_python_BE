from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from db.db_mongo.services_db.usuarios import obtener_usuario_db
from db.models.usuarios import Usuario_DB

ALGORITMO = "HS256"
DURACION_TOKEN = 240
LLAVE_SECRETA = "654aa6f819bd8e49753ddde2"

oauth2 = OAuth2PasswordBearer(tokenUrl="inicio_sesion")

crypt = CryptContext(schemes=["bcrypt"])

def validar_token(token: str = Depends(oauth2)) ->Usuario_DB:
    try:
        nombre_usuario = jwt.decode(token, LLAVE_SECRETA, algorithms=[ALGORITMO]).get("sub")
        usuario = obtener_usuario_db("nombre_usuario", nombre_usuario)
    except JWTError as e:
        raise str(e)

    return usuario

def desencriptar(pass_form: str, contrasennia: str) ->bool:

    return crypt.verify(pass_form, contrasennia)

def crear_token(access_token: dict) ->dict:

    return {"access_token": jwt.encode(access_token, LLAVE_SECRETA, algorithm=ALGORITMO), "token_type": "bearer"}

def crear_access_token(nombre_usuario: str) ->dict:

    return {
        "sub": nombre_usuario,
        "exp": datetime.utcnow() + timedelta(minutes= DURACION_TOKEN)
    }

def validar_admin(usuario_db: Usuario_DB = Depends(validar_token)) ->bool:
    resultado: bool = True
    if not usuario_db.tipo == "admin":
        resultado = False
    return resultado
    