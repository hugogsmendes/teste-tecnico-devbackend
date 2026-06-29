from sqlalchemy.ext.asyncio import AsyncSession
from src.models.tasks import Task
from sqlalchemy import select, Sequence
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