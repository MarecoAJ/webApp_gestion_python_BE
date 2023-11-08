from datetime import datetime
from typing import Optional
from schemas.usuarios import Usuario

class Usuario_DB(Usuario):
    fecha_insercion: Optional[datetime] = None
    estado: Optional[int] = None