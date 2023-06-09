from sqlalchemy import Column, Integer, String
from core.configs import Settings


class UsuarioModel(Settings.DBBaseModel):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(100), nullable=False)
    