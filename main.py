from fastapi import FastAPI
from middlewares.error_handler import ErrorHandler
from routers.marcas import marcas_router
from routers.modelos import modelos_router
from routers.usuarios import usuarios_router

# instancia de aplicacion
app = FastAPI()

# datos para documentacion Swagger
app.title = "Sistema de gestion"
app.version = "0.0.1"

#manejo de errores
app.add_middleware(ErrorHandler)

#routers del API
app.include_router(marcas_router)
app.include_router(modelos_router)
app.include_router(usuarios_router)
