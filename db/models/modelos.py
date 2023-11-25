from schemas.modelos import Modelos
from typing import Optional
from datetime import datetime

class Modelos_DB(Modelos):
    fecha_insercion: Optional[datetime] = None
    estado: Optional[int] = None