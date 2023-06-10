from models.livro_model import LivroModel
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from core.configs import settings

class EmprestimoModel(settings.DBBaseModel):
   __tablename__ = 'emprestimo'

   id = Column(Integer, primary_key=True, autoincrement=True)
   id_livro = Column(Integer, ForeignKey("livro.id"))
   id_usuario = Column(Integer, ForeignKey("usuario.id"))
   data_emprestimo = Column(DateTime)
   data_devolucao = Column(DateTime)

   livro = relationship("LivroModel", back_populates ="emprestimo", lazy ='joined')
   usuario = relationship("UsuarioModel", back_populates ="emprestimos", lazy ='joined')