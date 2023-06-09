from core.configs import Settings
from sqlalchemy import Column, Integer, String

class Categoria(Settings.DBBaseModel):
    __tablename__ = 'categoria'
    
    id: Column(Integer, primary_key=True, autoincrement=True)
    descricao: Column(String(100), nullable=False)