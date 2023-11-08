from typing import Optional
from pydantic import BaseModel

class Usuario(BaseModel):
    id: Optional[str] = None
    nombre_usuario: str
    contrasennia_usuario: str
    tipo: str