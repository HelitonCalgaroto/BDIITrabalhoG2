from models.emprestimo_model import EmprestimoModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.configs import Settings


class UsuarioModel(Settings.DBBaseModel):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(100), nullable=False)

    emprestimos = relationship("EmprestimoModel", 
                                cascade="all, delete-orphan", 
                                back_populates="usuario", 
                                uselist=True, 
                                lazy='joined'
                                )