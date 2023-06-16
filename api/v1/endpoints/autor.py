from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.future import select
from core.deps import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from models.autor_models import AutorModel
from schemas.autor_schema import AutorSchemaBase, AutorSchemaUp

router = APIRouter()


@router.get('/', response_model=List[AutorSchemaBase])
async def get_autores(db: AsyncSession = Depends(get_session)):
    async with db as session:
            query = select(AutorModel)
            result = await session.execute(query)
            autores: List[AutorSchemaBase] = result.scalars().unique().all()

    if autores:
        return autores
    else:
        raise HTTPException(detail="Nenhuma autor foi encontrado!",
                            status_code=status.HTTP_404_NOT_FOUND)


@router.get('/{autor_id}', 
            response_model=AutorSchemaBase, 
            status_code=status.HTTP_200_OK)
async def get_autor(autor_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel).filter(AutorModel.id == autor_id)
        result = await session.execute(query)
        autor: AutorSchemaBase = result.scalars().one_or_none()

    if autor:
        return autor
    else:
        raise HTTPException(detail="Autor não encontrado", 
                            status_code=status.HTTP_404_NOT_FOUND)


@router.post('/create', 
            status_code=status.HTTP_201_CREATED, 
            response_model=AutorSchemaBase)
async def post_autores(autor: AutorSchemaUp, 
                        db: AsyncSession = Depends(get_session)):
    novo_autor: AutorModel = AutorModel(nome=autor.nome)
    async with db as session:
        try:
            session.add(novo_autor)
            await session.commit()
            return novo_autor
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f'Autor já existe, {e}')


@router.put('/{autor_id}',
            response_model=AutorSchemaBase,
            status_code=status.HTTP_202_ACCEPTED)
async def put_autor(autor_id: int, 
                    autor: AutorSchemaUp, 
                    db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel).filter(AutorModel.id == autor_id)
        result = await session.execute(query)
        autor_up: AutorSchemaBase = result.scalars().unique().one_or_none()
    
    if autor_up:
        if autor.nome:
            autor_up.nome = autor.nome
        return autor_up
    else:
        raise HTTPException(detail="Autor não encontrado",
                            status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{autor_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_autor(autor_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AutorModel).filter(AutorModel.id == autor_id)
        result = await session.execute(query)
        autor_del: AutorSchemaBase = result.scalars().one_or_none()

    if autor_del:
        await session.delete(autor_del)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(detail="Autor não encontrado",
                            status_code=status.HTTP_404_NOT_FOUND)
