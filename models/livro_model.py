from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from core.configs import settings

class LivroModel(settings.DBBaseModel):
   __tablename__ = 'livro'

   id = Column(Integer, primary_key=True, index=True)
   titulo = Column(String(255), nullable=False)
   id_categoria = Column(Integer, ForeignKey('categoria.id'))
   id_autor = Column(Integer, ForeignKey('autor.id'))

   categoria = relationship('CategoriaModel', back_populates="livro")
   autor = relationship('AutorModel', back_populates="livro")
   
   emprestimo = relationship('EmprestimoModel', back_populates="livro")