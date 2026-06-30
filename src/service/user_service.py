from src.repository.user_repository import UserRepository
from fastapi import status, HTTPException
from src.utils.security import verify_password, create_token_jwt

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def login (self, email: str, password: str) -> dict:
        try:
            user = await self.repository.get_user_by_email(email)

            if not user:
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Credencias inválidas")
            
            if not verify_password(user.senha_hash, password):
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Credencias inválidas")
            
            token = create_token_jwt(user.id, user.nome, user.email)

            return {"token": token}   
        
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")
