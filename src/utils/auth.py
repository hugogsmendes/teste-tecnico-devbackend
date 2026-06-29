from fastapi import Depends, status, HTTPException, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.security import verify_token_jwt
from src.core.config import Settings

setting = Settings()
security = HTTPBearer(auto_error = False)

async def get_current_user(request: Request, credential: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = request.cookies.get("auth")
        if not token:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Não autenticado")
    
        payload = verify_token_jwt(token, "access")

        if not payload:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Não autenticado")

        
        return {
            "id": payload.get("sub"),
            "nome": payload.get("name"),
            "email": payload.get("email"),
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException 