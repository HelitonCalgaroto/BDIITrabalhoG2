from fastapi import APIRouter

from api.v1.endpoints import usuario, categoria, autor, livro

api_router = APIRouter()
api_router.include_router(usuario.router, prefix='/usuarios', tags=['Usuarios'])
api_router.include_router(categoria.router, prefix='/categoria', tags=['Categoria'])
api_router.include_router(autor.router, prefix='/autor', tags=['Autor'])
api_router.include_router(livro.router, prefix='/livro', tags=['Livro'])

# api_router.include_router(
#     categoria.router, prefix='/categorias', tags=['Categorias']
# )