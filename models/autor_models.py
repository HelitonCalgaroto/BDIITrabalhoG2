from core.configs import Settings
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

class AutorModel(Settings.DBBaseModel):
    __tablename__ = "autor"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)

    livro = relationship('LivroModel', back_populates="autor")