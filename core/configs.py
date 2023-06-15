from pydantic import BaseSettings
from sqlalchemy.ext.declarative  import declarative_base

class Settings(BaseSettings):
    '''configuracoes gerais da API'''
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'mysql+aiomysql://yourbook:yourbook@localhost:3306/yourbook'
    DBBaseModel = declarative_base()

    '''
    import secrets
    token: str = secrets.token_urlsafe(32)  
    print(token)
    '''

    JWT_SECRET: str = 'GjiJz4N4uHnVP4xFDAaipU2ExjjVekeaKxBuSlCqkfk'
    ALGORITHM: str = 'HS256'
    # Minuts
    ACESS_TOKEN_EXPIRE_MINUTS: int = 7 * 24 * 60
    
    class Config:
        case_sensitive = True
        
settings = Settings()
