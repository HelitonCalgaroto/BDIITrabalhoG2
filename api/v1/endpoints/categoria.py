from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.future import select
from core.deps import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from schemas.categoria_schema import CategoriaSchemaBase, CategoriaSchemaUp
from models.categoria_models import CategoriaModel

router = APIRouter()


@router.get('/', response_model=CategoriaSchemaBase)
async def get_categorias(db: AsyncSession = Depends(get_session)):
    async with db as session:
            query = select(CategoriaModel)
            result = await session.execute(query)
            categorias: List[CategoriaSchemaBase] = result.scalars().unique().all()

    if categorias:
        return categorias
    else:
        raise HTTPException(detail="Nenhuma categoria foi encontrada!",
                            status_code=status.HTTP_404_NOT_FOUND)

@router.get('/{categoria_id}', 
            response_model=CategoriaSchemaBase, 
            status_code=status.HTTP_200_OK)
async def get_categoria(categoria_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel).filter(CategoriaModel.id == categoria_id)
        result = await session.execute(query)
        categoria: CategoriaSchemaBase = result.scalars().one_or_none()

    if categoria:
        return categoria
    else:
        raise HTTPException(detail="Categoria não encontrada!", 
                            status_code=status.HTTP_404_NOT_FOUND)


@router.post('/create', 
            status_code=status.HTTP_201_CREATED, 
            response_model=CategoriaSchemaBase)
async def post_categoria(categoria: CategoriaSchemaUp,
                        db: AsyncSession = Depends(get_session)):
    nova_categoria: CategoriaModel = CategoriaModel(nome=categoria.nome)
    async with db as session:
        try:
            session.add(nova_categoria)
            await session.commit()
            return nova_categoria
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'Ja existe essa categoria cadastrada, {e}')


@router.put('/{categoria_id}',
            response_model=CategoriaSchemaBase,
            status_code=status.HTTP_202_ACCEPTED)
async def put_categoria(categoria_id: int,
                        categoria: CategoriaSchemaUp,
                        db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel).filter(CategoriaModel.id == categoria_id)
        result = await session.execute(query)
        categoria_up: CategoriaSchemaBase = result.scalars().unique().one_or_none()
    
    if categoria_up:
        if categoria.nome:
            categoria_up.nome = categoria.nome
        return categoria_up
    else:
        raise HTTPException(detail="Categoria não encontrada",
                            status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{categoria_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(categoria_id: int, 
                            db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CategoriaModel).filter(CategoriaModel.id == categoria_id)
        result = await session.execute(query)
        categoria_del: CategoriaSchemaBase = result.scalars().one_or_none()

    if categoria_del:
        await session.delete(categoria_del)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(detail="Categoria não encontrada",
                            status_code=status.HTTP_404_NOT_FOUND)
