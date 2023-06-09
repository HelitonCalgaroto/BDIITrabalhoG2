from typing import Optional
from pydantic import BaseModel

class CategoriaSchema(BaseModel):
    id: Optional[int] = None
    descricao: str
    
    class Config:
        orm_mode = True
        