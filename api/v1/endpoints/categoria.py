from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.future import select
from core.deps import get_session
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from schemas.categoria_schema import CategoriaSchema
from models.categoria_models import CategoriaModel

router = APIRouter()

@router.get('/', response_model=None)
async def get_categorias(db: AsyncSession = Depends(get_session)):
    async with db as session:
            query = select(CategoriaModel)
            result = await session.execute(query)
            categorias: List[CategoriaSchema] = result.scalars().unique().all()
            return categorias

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=None)
async def post_categoria(categoria: CategoriaSchema,
                db: AsyncSession = Depends(get_session)):
    nova_categoria: CategoriaModel = CategoriaModel(nome=categoria.nome,
                                                )
    async with db as session:
        try:
            session.add(nova_categoria)
            await session.commit()
            return nova_categoria
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Ja existe essa categoria cadastrada, {e}')

@router.put('/{categoria_id}',
            response_model=None,
            status_code=status.HTTP_202_ACCEPTED)
async def put_categoria(categoria_id: int,
                    categoria: CategoriaSchema,
                    db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel).filter(CategoriaModel.id == categoria_id)
        result = await session.execute(query)
        categoria_up: CategoriaSchema = result.scalars().unique().one_or_none()
    
    if categoria_up:
        if categoria.nome:
            categoria_up.nome = categoria.nome
        return categoria_up
    else:
        raise HTTPException(detail="Categoria não encontrada",
                            status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{categoria_id}', status_code=status.HTTP_404_NOT_FOUND)
async def delete_usuario(categoria_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel).filter(CategoriaModel.id == categoria_id)
        result = await session.execute(query)
        categoria_del: CategoriaSchema = result.scalars().one_or_none()

    if categoria_del:
        await session.delete(categoria_del)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(detail="Categoria não encontrada",
                            status_code=status.HTTP_404_NOT_FOUND)

@router.get('/{categoria_id}', response_model=None, status_code=status.HTTP_200_OK)
async def get_categoria(categoria_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel).filter(CategoriaModel.id == categoria_id)
        result = await session.execute(query)
        categoria: CategoriaSchema = result.scalars().one_or_none()

    if categoria:
        return categoria
    else:
        raise HTTPException(detail="Usuario não encontrado", status_code=status.HTTP_404_NOT_FOUND)
