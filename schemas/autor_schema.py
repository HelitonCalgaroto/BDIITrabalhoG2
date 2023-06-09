from typing import Optional
from pydantic import BaseModel

class AutorSchema(BaseModel):
    
    id: Optional[int] = None
    nome: str