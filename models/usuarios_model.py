from sqlalchemy import Column, Integer, String
from core.configs import Settings
from core.configs import Settings
from sqlalchemy.orm import relationship

class UsuarioModel(Settings.DBBaseModel):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(100), nullable=False)
    
    emprestimo = relationship('EmprestimoModel', back_populates="usuario")