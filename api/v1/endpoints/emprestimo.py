from typing import List
from sqlalchemy.future import select
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from models.emprestimo_model import EmprestimoModel
from schemas.emprestimo_schema import EmprestimoSchemaBase, EmprestimoSchemaUp


router =APIRouter()


@router.get('/', response_model=List[EmprestimoSchemaBase])
async def get_emprestimos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EmprestimoModel)
        result = await session.execute(query)
        emprestimos: List[EmprestimoSchemaBase] = result.scalars().all()
        return emprestimos
    

@router.get('/{emprestimo_id}', status_code=status.HTTP_200_CREATED, response_model=EmprestimoSchemaBase)
async def get_emprestimo(emprestimo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EmprestimoModel).filter(EmprestimoModel.id == emprestimo_id)
        result = await session.execute(query)
        emprestimo: EmprestimoSchemaBase = result.scalars().one_or_none()
        
        if emprestimo:
            return emprestimo
        else:
            raise HTTPException(detail="Emprestimo não encontrado",status_code=status.HTTP_404_NOT_FOUND)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=EmprestimoSchemaBase)
async def post_emprestimo(emprestimo: EmprestimoSchemaUp, db: AsyncSession = Depends(get_session)):
    novo_emprestimo: EmprestimoModel = EmprestimoModel(id_livro=emprestimo.id_livro,
                                                       id_usuario=emprestimo.id_usuario,
                                                       data_emprestimo=emprestimo.data_emprestimo,
                                                       data_devolucao=emprestimo.data_devolucao)
    async with db as session:
        try:
            session.add(novo_emprestimo)
            await session.commit()
            return novo_emprestimo
        except (Exception) as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"Emprestimo já existente, {e}")
            

@router.put('/{emprestimo_id}', status_code=status.HTTP_202_ACCEPTED, response_model=EmprestimoSchemaBase)
async def put_emprestimo(emprestimo_id: int, emprestimo: EmprestimoSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EmprestimoModel).filter(EmprestimoModel.id == emprestimo_id)
        result = await session.execute(query)
        emprestimo_up: EmprestimoSchemaBase = result.scalars().one_or_none()
        
        if emprestimo_up:
            if emprestimo.id_livro:
                emprestimo.id_livro = emprestimo.id_livro
            if emprestimo.id_usuario:
                emprestimo.id_usuario = emprestimo.id_usuario
            if emprestimo.data_emprestimo:
                emprestimo.data_emprestimo = emprestimo.data_emprestimo
            if emprestimo.data_devolucao:
                emprestimo.data_devolucao = emprestimo.data_devolucao
            return emprestimo_up
        else:
            raise HTTPException(detail="Emprestimo não encontrado", 
                                status_code=status.HTTP_404_NOT_FOUND)
            
            
@router.delete('/{emprestimo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_emprestimo(emprestimo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(EmprestimoModel).filter(EmprestimoModel.id == emprestimo_id)
        result = await session.execute(query)
        emprestimo_del: EmprestimoSchemaBase = result.scalars().one_or_none()
        
        if emprestimo_del:
            await session.delete(emprestimo_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Emprestimo não encontrado", 
                                status_code=status.HTTP_404_NOT_FOUND)
            