from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from core.configs import settings

class LivroModel(settings.DBBaseModel):
   __tablename__ = 'livro'

   id = Column(Integer, primary_key=True, index=True)
   titulo = Column(String(255), nullable=False)
   id_categoria = Column(Integer, ForeignKey('categoria.id'))
   id_autor = Column(Integer, ForeignKey('autor.id'))

   categoria = relationship('Categoria', back_populates='livros')
   autor = relationship('Autor', back_populates='livros')