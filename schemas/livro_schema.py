from typing import Optional
from pydantic import BaseModel

class LivroSchemaBase(BaseModel):
    id: Optional[int] = None
    titulo: str
    id_categoria: int
    id_autor: int

    class Config:
        orm_mode = True
        
class LivroSchemaUp(LivroSchemaBase):
    titulo: Optional[str]
    id_categoria: Optional[int]
    id_autor: Optional[int]
