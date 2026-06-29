from src.repository.task_repository import TaskRepository
from src.utils.schemas import CriarTarefa
from fastapi import HTTPException, status
class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task (self, tarefa: CriarTarefa):

        try:
            tarefa_dict = tarefa.model_dump()

            return await self.repository.create_task(tarefa_dict)

        except HTTPException:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")
        except Exception:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")
        
    async def list_tasks (self):

        try:

            return await self.repository.list_tasks()

        except HTTPException:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")
        except Exception:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")
