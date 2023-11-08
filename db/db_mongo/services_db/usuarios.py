from db.db_mongo.conexion_mongo import db_cliente as db
from db.models.usuarios import Usuario_DB

def obtener_usuario_db(campo: str, valor) -> Usuario_DB:
    try: 
        resultado_db = db.web_gestion.usuarios.find_one({campo: valor})
        usuario_db = usuario_model(resultado_db)
        if not usuario_db:
            return ""
        else:
            return usuario_db
    except ConnectionError as e:
       return str(e)
    
def usuario_model(usuario_db: dict) ->Usuario_DB:   
    usuario = {
        "id": str(usuario_db["_id"]),
        "nombre_usuario": usuario_db["nombre_usuario"],
        "contrasennia_usuario": usuario_db["contrasennia_usuario"],
        "tipo": usuario_db["tipo"],
        "fecha_insercion": usuario_db["fecha_insercion"],
        "estado": usuario_db["estado"]
    }
    return Usuario_DB(**usuario)