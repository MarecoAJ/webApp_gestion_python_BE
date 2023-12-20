from typing import Optional
from pydantic import BaseModel

class Productos(BaseModel):
    id: Optional[str] = None
    descrip_produc: str 
    modelo_id: str
    cant_produc: int
    min_cant_produc: int
