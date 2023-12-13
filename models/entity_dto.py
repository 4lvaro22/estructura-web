from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Entity (BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    images: Optional[str] #list[str]
    latitud: float
    longitud: float
    direccion: str

    
class EntityForm (BaseModel):
    name: str
    description: str
