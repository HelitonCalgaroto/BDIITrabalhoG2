from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class EmprestimoSchema(BaseModel):
   id: Optional[int] = None
   id_livro: int
   id_usuario: int
   data_emprestimo: Optional[datetime] = None
   data_devolucao: Optional[datetime] = None

   class Config:
      orm_mode = True