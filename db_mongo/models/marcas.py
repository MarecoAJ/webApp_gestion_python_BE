from datetime import datetime
from typing import Optional
from schemas.marcas import Marcas

class Marcas_DB(Marcas):
    fecha_insercion: Optional[datetime] = None
    estado: Optional[int] = None