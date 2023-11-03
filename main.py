from fastapi import FastAPI
from middlewares.error_handler import ErrorHandler
from routers.marcas import marcas_router

# instancia de aplicacion
app = FastAPI()

# datos para documentacion Swagger
app.title = "Sistema de gestion"
app.version = "0.0.1"

#manejo de errores
app.add_middleware(ErrorHandler)

#routers del API
app.include_router(marcas_router)