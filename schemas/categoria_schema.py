from typing import Optional
from pydantic import BaseModel

class CategoriaSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str

    class Config:
        orm_mode = True

class CategoriaSchemaUp(CategoriaSchemaBase):
    nome: Optional[str]
    