from typing import Optional
from pydantic import BaseModel

class AutorSchemaBase(BaseModel):
    
    id: Optional[int] = None
    nome: str
    
    class Config:
        orm_mode = True

class AutorSchemaUp(AutorSchemaBase):
    nome: Optional[str]
