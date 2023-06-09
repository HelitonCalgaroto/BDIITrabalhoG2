from core.configs import Settings
from sqlalchemy import Column, Integer, String

class Autor(Settings.DBBaseModel):
    __tablename__ = "autor"
    
    id: Column(Integer, primary_key=True, autoincrement=True)
    nome: Column(String(30), nullable=False)