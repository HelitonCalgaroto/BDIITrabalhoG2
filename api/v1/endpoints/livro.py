from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.future import select
from core.deps import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from models.livro_model import LivroModel

from models.autor_models import AutorModel
from models.categoria_models import CategoriaModel

from schemas.livro_schema import LivroSchemaBase, LivroSchemaUp

router = APIRouter()


@router.get('/', response_model=List[LivroSchemaBase])
async def get_livros(db: AsyncSession = Depends(get_session)):
    async with db as session:
            query = select(LivroModel)
            result = await session.execute(query)
            livros: List[LivroSchemaBase] = result.scalars().unique().all()

    if livros:
        return livros
    else:
        raise HTTPException(detail="Nenhum livro foi encontrado!",
                            status_code=status.HTTP_404_NOT_FOUND)

@router.get('/{livro_id}', 
            response_model=LivroSchemaBase, 
            status_code=status.HTTP_200_OK)
async def get_livro(livro_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivroModel).filter(LivroModel.id == livro_id)
        result = await session.execute(query)
        livro: LivroSchemaBase = result.scalars().unique().one_or_none()

    if livro:
        return livro
    else:
        raise HTTPException(detail="Livro não encontrado", 
                            status_code=status.HTTP_404_NOT_FOUND)


@router.post('/create', 
            status_code=status.HTTP_201_CREATED, 
            response_model=LivroSchemaBase)
async def post_livro(livro: LivroSchemaUp,
                    db: AsyncSession = Depends(get_session)):

    categoria = await db.get(CategoriaModel, livro.id_categoria)

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Categoria não encontrada')

    autor = await db.get(AutorModel, livro.id_autor)

    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Autor não encontrada')

    novo_livro: LivroModel = LivroModel(titulo=livro.titulo,
                                        categoria=categoria,
                                        autor=autor,
                                        imagem=livro.imagem)
    async with db as session:
        try:
            session.add(novo_livro)
            await session.commit()
            return novo_livro
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'Livro já existente, {e}')


@router.put('/{livro_id}',
            response_model=LivroSchemaBase,
            status_code=status.HTTP_202_ACCEPTED)
async def put_livro(livro_id: int,
                    livro: LivroSchemaUp,
                    db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivroModel).filter(LivroModel.id == livro_id)
        result = await session.execute(query)
        livro_up: LivroSchemaBase = result.scalars().unique().one_or_none()

    if livro_up:
        if livro.titulo:
            livro_up.titulo = livro.titulo
        if livro.id_categoria:
            livro_up.id_categoria = livro.id_categoria
        if livro.id_autor:
            livro_up.id_autor = livro.id_autor
        if livro.imagem:
            livro_up.imagem = livro.imagem
        await session.merge(livro_up)
        await session.commit()
        return livro_up
    else:
        raise HTTPException(detail="Livro não encontrado",
                            status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{livro_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_livro(livro_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LivroModel).filter(LivroModel.id == livro_id)
        result = await session.execute(query)
        livro_del: LivroSchemaBase = result.scalars().unique().one_or_none()

    if livro_del:
        await session.delete(livro_del)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(detail="Livro não encontrado",
                            status_code=status.HTTP_404_NOT_FOUND)
