from pydantic import BaseModel
from typing import Optional


class Modelos(BaseModel):
    id: Optional[str] = None
    descrip_modelo: str
    marca_id: str