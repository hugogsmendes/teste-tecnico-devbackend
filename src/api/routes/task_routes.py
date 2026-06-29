from fastapi import APIRouter, Depends, status
from src.service.task_service import TaskService
from src.utils.dependencies import get_task_service
from src.utils.schemas import CriarTarefa, ResponseMensagemErro, ResponseTarefa, AtualizarTarefa

task_router = APIRouter(prefix = "/task", tags = ["tasks"])

task_create_responses = {
    201: {"model": ResponseTarefa, "description": "Tarefa criada"},
    500: {"model": ResponseMensagemErro, "description": "Erro interno"},
}

task_list_responses = {
    200: {"model": list[ResponseTarefa], "description": "Tarefas listada"},
    404: {"model": ResponseMensagemErro, "description": "Tarefas não encontradas"},
    500: {"model": ResponseMensagemErro, "description": "Erro interno"},
}

task_list_by_id_responses = {
    200: {"model": list[ResponseTarefa], "description": "Tarefa listada"},
    404: {"model": ResponseMensagemErro, "description": "Tarefa não encontrada"},
    500: {"model": ResponseMensagemErro, "description": "Erro interno"},
}

task_update_responses = {
    204: {"model": None, "description": "Tarefa atualizada"},
    404: {"model": ResponseMensagemErro, "description": "Tarefa não encontrada"},
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

@task_router.get(path = "",
                 summary = "Lista as tarefas",
                 description = "Lista as tarefas de acordo com filtros",
                 response_model = list[ResponseTarefa],
                 responses = task_list_responses,
                 status_code = status.HTTP_200_OK)
async def list_tasks (service: TaskService = Depends(get_task_service)):
    return await service.list_tasks()

@task_router.get(path = "/{id}",
                 summary = "Lista tarefa pelo ID",
                 description = "Lista a tarefa pelo ID passado na requisição",
                 response_model = ResponseTarefa,
                 responses = task_list_by_id_responses,
                 status_code = status.HTTP_200_OK)
async def list_task_by_id (id: int, service: TaskService = Depends(get_task_service)):
    return await service.list_tasks_by_id(id)

@task_router.patch(path = "/{id}",
                   summary = "Atualiza uma tarefa pelo ID",
                   description = "Atualiza parcialmente de acordo com os campos enviados",
                   responses = task_update_responses,
                   status_code = status.HTTP_204_NO_CONTENT)
async def update_task_by_id (id: int, tarefa: AtualizarTarefa, service: TaskService = Depends(get_task_service)):
    return await service.update_task_by_id(id, tarefa)