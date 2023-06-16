from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.future import select
from core.deps import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from models.autor_models import AutorModel
from schemas.autor_schema import AutorSchema
router = APIRouter()

@router.get('/', response_model=None)

async def get_autores(db: AsyncSession = Depends(get_session)):
    async with db as session:
            query = select(AutorModel)
            result = await session.execute(query)
            autores: List[AutorSchema] = result.scalars().unique().all()
            return autores

@router.get('/{autor_id}', response_model=None, status_code=status.HTTP_200_OK)
async def get_autor(autor_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel).filter(AutorModel.id == autor_id)
        result = await session.execute(query)
        autor: AutorSchema = result.scalars().one_or_none()

    if autor:
        return autor
    else:
        raise HTTPException(detail="Autor não encontrado", status_code=status.HTTP_404_NOT_FOUND)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=None)
async def post_autores(autor: AutorSchema,
                db: AsyncSession = Depends(get_session)):
    nova_autor: AutorModel = AutorModel(nome=autor.nome,
                                                )
    async with db as session:
        try:
            session.add(nova_autor)
            await session.commit()
            return nova_autor
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Ja existe essa autor cadastrada, {e}')

@router.put('/{autor_id}',
            response_model=None,
            status_code=status.HTTP_202_ACCEPTED)
async def put_autor(autor_id: int,
                        autor: AutorSchema,
                        db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel).filter(AutorModel.id == autor_id)
        result = await session.execute(query)
        autor_up: AutorSchema = result.scalars().unique().one_or_none()
    
    if autor_up:
        if autor.nome:
            autor_up.nome = autor.nome
        return autor_up
    else:
        raise HTTPException(detail="Autor não encontrada",
                            status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{autor_id}', status_code=status.HTTP_404_NOT_FOUND)
async def delete_autor(autor_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel).filter(AutorModel.id == autor_id)
        result = await session.execute(query)
        autor_del: AutorSchema = result.scalars().one_or_none()

    if autor_del:
        await session.delete(autor_del)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(detail="Autor não encontrada",
                            status_code=status.HTTP_404_NOT_FOUND)

