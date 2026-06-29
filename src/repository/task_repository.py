from sqlalchemy.ext.asyncio import AsyncSession
from src.models.tasks import Task
from sqlalchemy import select, Sequence
from datetime import datetime
class TaskRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task (self, tarefa_dict: dict) -> Task:

        try:

            new_task = Task(**tarefa_dict)

            self.session.add(new_task)
            await self.session.commit()
            await self.session.refresh(new_task)

            return new_task
        
        except Exception:

            await self.session.rollback()
            raise
    
    async def list_tasks (self) -> Sequence[Task]:

        stmt = select(Task)

        result = await self.session.execute(stmt)

        return result.scalars().all()
    
    async def get_task_by_id (self, id: int) -> Task | None:

        stmt = select(Task).filter(Task.id == id)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
    
    async def update_task_by_id (self, task: Task, tarefa_dict: dict) -> None:

        try:

            for field, value in tarefa_dict.items():
                setattr(task, field, value)

            await self.session.commit()
            await self.session.refresh(task)

        except Exception:

            await self.session.rollback()
            raise

    async def delete_task_by_id (self, task: Task) -> None:

        try:

            task.data_de_exclusao = datetime.now()
            await self.session.commit()
            await self.session.refresh(task)

        except Exception:
            await self.session.rollback()
            raise