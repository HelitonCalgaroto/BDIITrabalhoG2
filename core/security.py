from passlib.context import CryptContext

CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verificar_senha(senha: str, hash_senha: str) -> bool:
   '''
   Função para verificar se a senha está correta, comparando a senha com o hash.
   '''
   return CRYPTO.verify(senha, hash_senha)

def gerar_hash_senha(senha: str) -> str:
   '''
   Função para gerar e retornar o hash da senha.
   '''
   return CRYPTO.hash(senha)