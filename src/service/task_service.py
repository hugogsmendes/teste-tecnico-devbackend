from src.repository.task_repository import TaskRepository
from src.utils.schemas import CriarTarefa, AtualizarTarefa, StatusTarefa
from fastapi import HTTPException, status
class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task (self, tarefa: CriarTarefa):

        try:
            tarefa_dict = tarefa.model_dump()

            return await self.repository.create_task(tarefa_dict)

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")
        
    async def list_tasks (self, status_tarefa: StatusTarefa | None, titulo_tarefa: str | None):

        try:

            return await self.repository.list_tasks(status_tarefa, titulo_tarefa)

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")

        
    async def list_tasks_by_id (self, id: int):

        try:

            task = await self.repository.get_task_by_id(id)

            if not task:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Tarefa não encontrada")
            
            return task

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")
        
            
    async def update_task_by_id (self, id: int, tarefa: AtualizarTarefa):

        try:
            tarefa_dict = tarefa.model_dump(exclude_none = True)
            if not tarefa_dict:
                return
            
            task = await self.repository.get_task_by_id(id)

            if not task:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Tarefa não encontrada")
            
            return await self.repository.update_task_by_id(task, tarefa_dict)
        
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")
        
    async def delete_task_by_id (self, id: int):

        try:

            task = await self.repository.get_task_by_id(id)

            if not task:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Tarefa não encontrada")
            
            return await self.repository.delete_task_by_id(task)
        
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Erro interno")