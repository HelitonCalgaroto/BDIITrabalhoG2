from typing import Optional
from pydantic import BaseModel

class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    
    class Config:
        orm_mode = True

class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    
class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str
