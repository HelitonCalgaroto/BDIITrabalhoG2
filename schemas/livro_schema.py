from typing import Optional
from pydantic import BaseModel

class LivroSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    id_categoria: int
    id_autor: int

    class Config:
        orm_mode = True