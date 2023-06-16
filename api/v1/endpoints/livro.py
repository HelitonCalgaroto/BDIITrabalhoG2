from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.future import select
from core.deps import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from models.livro_model import LivroModel
from models.categoria_models import CategoriaModel
from models.autor_models import AutorModel
from schemas.livro_schema import LivroSchema

router = APIRouter()

@router.get('/', response_model=None)
async def get_livros(db: AsyncSession = Depends(get_session)):
    async with db as session:
            query = select(LivroModel)
            result = await session.execute(query)
            livros: List[LivroSchema] = result.scalars().unique().all()
            return livros

@router.get('/{livro_id}', response_model=None, status_code=status.HTTP_200_OK)
async def get_livro(livro_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivroModel).filter(LivroModel.id == livro_id)
        result = await session.execute(query)
        livro: LivroSchema = result.scalars().one_or_none()

    if livro:
        return livro
    else:
        raise HTTPException(detail="Livro não encontrado", status_code=status.HTTP_404_NOT_FOUND)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=None)
async def post_livro(livro: LivroSchema,
                db: AsyncSession = Depends(get_session)):
    
    categoria = await db.get(CategoriaModel, livro.id_categoria)

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Categoria não encontrada')
          
    autor = await db.get(AutorModel, livro.id_autor)

    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Autor não encontrada')
    
    nova_livro: LivroModel = LivroModel(titulo=livro.titulo,
                                        categoria=categoria,
                                        autor=autor
                                                )
    async with db as session:
        try:
            session.add(nova_livro)
            await session.commit()
            return nova_livro
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Ja existe essa livro cadastrada, {e}')

@router.put('/{livro_id}',
            response_model=None,
            status_code=status.HTTP_202_ACCEPTED)
async def put_livro(livro_id: int,
                        livro: LivroSchema,
                        db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivroModel).filter(LivroModel.id == livro_id)
        result = await session.execute(query)
        livro_up: LivroSchema = result.scalars().unique().one_or_none()
    
    if livro_up:
        if livro.titulo:
            livro_up.titulo = livro.titulo
            
            
        if livro.id_categoria:
            livro_up.id_categoria = livro.id_categoria
            
        
        if livro.id_autor:
            livro_up.id_autor = livro.id_autor
            
        return livro_up
    else:
        raise HTTPException(detail="Livro não encontrada",
                            status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{livro_id}', status_code=status.HTTP_404_NOT_FOUND)
async def delete_livro(livro_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivroModel).filter(LivroModel.id == livro_id)
        result = await session.execute(query)
        livro_del: LivroSchema = result.scalars().one_or_none()

    if livro_del:
        await session.delete(livro_del)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(detail="Livro não encontrada",
                            status_code=status.HTTP_404_NOT_FOUND)