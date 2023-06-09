from fastapi import APIRouter

from api.v1.endpoints import usuario, categoria

api_router = APIRouter()
api_router.include_router(usuario.router, prefix='/usuarios', tags=['Usuarios'])
api_router.include_router(categoria.router, prefix='/categoria', tags=['Categoria'])

api_router.include_router(
    categoria.router, prefix='/categorias', tags=['Categorias']
)