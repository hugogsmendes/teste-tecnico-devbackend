from fastapi import APIRouter, Depends, status
from src.service.task_service import TaskService
from src.utils.dependencies import get_task_service
from src.utils.schemas import CriarTarefa, ResponseMensagemErro, ResponseTarefa

task_router = APIRouter(prefix = "/task", tags = ["tasks"])

task_create_responses = {
    201: {"model": ResponseTarefa, "description": "Tarefa criada com sucesso"},
    500: {"model": ResponseMensagemErro, "description": "Erro interno"},
}

@task_router.post(path = "", 
                  summary =  "Cria uma nova tarefa",
                  description = "Recebe os dados e cria uma nova tarefa",
                  response_model = ResponseTarefa,
                  responses = task_create_responses,
                  status_code = status.HTTP_201_CREATED)
async def create_task (tarefa: CriarTarefa, service: TaskService = Depends(get_task_service)):
    return await service.create_task(tarefa)