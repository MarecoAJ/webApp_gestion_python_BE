from fastapi import FastAPI
from middlewares.error_handler import ErrorHandler

# instancia de aplicacion
app = FastAPI()

# datos para documentacion Swagger
app.title = "Sistema de gestion"
app.version = "0.0.1"

#manejo de errores
app.add_middleware(ErrorHandler)