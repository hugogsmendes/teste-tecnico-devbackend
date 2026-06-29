from fastapi import APIRouter, Depends, status, Query
from typing import Optional
from src.service.task_service import TaskService
from src.utils.dependencies import get_task_service
from src.utils.auth import get_current_user
from src.utils.schemas import CriarTarefa, ResponseMensagemErro, ResponseTarefa, AtualizarTarefa, StatusTarefa

task_router = APIRouter(prefix = "/task", tags = ["tasks"], dependencies = [Depends(get_current_user)])

task_create_responses = {
    201: {"model": ResponseTarefa, "description": "Tarefa criada"},
    401: {"model": ResponseMensagemErro, "description": "Não autenticado"},
    500: {"model": ResponseMensagemErro, "description": "Erro interno"},
}

task_list_responses = {
    200: {"model": list[ResponseTarefa], "description": "Tarefas listada"},
    401: {"model": ResponseMensagemErro, "description": "Não autenticado"},
    404: {"model": ResponseMensagemErro, "description": "Tarefas não encontradas"},
    500: {"model": ResponseMensagemErro, "description": "Erro interno"},
}

task_list_by_id_responses = {
    200: {"model": list[ResponseTarefa], "description": "Tarefa listada"},
    401: {"model": ResponseMensagemErro, "description": "Não autenticado"},
    404: {"model": ResponseMensagemErro, "description": "Tarefa não encontrada"},
    500: {"model": ResponseMensagemErro, "description": "Erro interno"},
}

task_update_responses = {
    204: {"model": None, "description": "Tarefa atualizada"},
    401: {"model": ResponseMensagemErro, "description": "Não autenticado"},
    404: {"model": ResponseMensagemErro, "description": "Tarefa não encontrada"},
    500: {"model": ResponseMensagemErro, "description": "Erro interno"},
}

task_delete_responses = {
    204: {"model": None, "description": "Tarefa deletada"},
    401: {"model": ResponseMensagemErro, "description": "Não autenticado"},
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
async def list_tasks (status_tarefa: Optional[StatusTarefa] = Query(None, description = "Filtre por: Pendente, Em andamento ou Concluída"),
                      titulo_tarefa: Optional[str] = Query(None, description = "Busque por uma palavra no título"),
                      limit: int = Query(5, ge = 1, le = 20, description = "Quantidade de itens por página"),
                      offset: int = Query(0, ge = 0, description = "Quantidade de itens para pular"),
                      service: TaskService = Depends(get_task_service)):
    return await service.list_tasks(status_tarefa, titulo_tarefa, limit, offset)

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

@task_router.delete(path = "{id}",
                    summary = "Deleta uma tarefa pelo ID",
                    description = "Deleta uma tarefa",
                    responses = task_delete_responses,
                    status_code = status.HTTP_204_NO_CONTENT)
async def delete_task_by_id (id: int, service: TaskService = Depends(get_task_service)):
    return await service.delete_task_by_id(id)