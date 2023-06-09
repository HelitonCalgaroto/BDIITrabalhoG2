#pip install fastapi uvicorn sqlalchemy pydantic gunicorn autopep8 anyio email-validator cryptography aiomysql pymysql  (instalacao de dependencias)
#pip freeze > requirements.txt (cria um arquivo para ficar salvo as versoes do projeto)

from fastapi import APIRouter, FastAPI
from api.v1.api import api_router

from core.configs import settings

app = FastAPI(title='YourBook - Para todos aqueles que gostam de ler!')
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',
                host="0.0.0.0",
                port=8000,
                log_level="info",
                reload=True
                )
