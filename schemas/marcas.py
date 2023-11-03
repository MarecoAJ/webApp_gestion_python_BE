from typing import Optional
from pydantic import BaseModel

class Marcas(BaseModel):
    id: Optional[str] = None
    descrip_marca: str