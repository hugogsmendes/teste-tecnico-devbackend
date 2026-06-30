from fastapi import APIRouter, Depends, status, Response
from src.utils.schemas import ResponseMensagemErro
from fastapi.security import OAuth2PasswordRequestForm
from src.service.user_service import UserService
from src.utils.dependencies import get_user_service
from src.utils.auth import set_cookie_auth

auth_router = APIRouter(prefix = "/auth", tags = ["auth"])

auth_login_responses = {
    204: {"model": None, "description": "Login realizado"},
    401: {"model": ResponseMensagemErro, "description": "Credencias inválidas"},
    500: {"model": ResponseMensagemErro, "description": "Erro interno"},
}

@auth_router.post(path = "/login",
                  summary = "Realiza o login",
                  description = "Login com email e senha",
                  responses = auth_login_responses,
                  status_code = status.HTTP_204_NO_CONTENT)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service)):
    res = await service.login(form_data.username, form_data.password)
    set_cookie_auth(response, res.get("token"))