from schemas.productos import Productos
from typing import Optional
from datetime import datetime

class Productos_DB(Productos):
    fecha_insercion: Optional[datetime]  = None
    estado: Optional[int] = None