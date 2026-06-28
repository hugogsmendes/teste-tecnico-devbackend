from src.database.db import SessionLocal
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.task_repository import TaskRepository
from src.service.task_service import TaskService
from fastapi import Depends

async def get_session () -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_task_repository (session: AsyncSession = Depends(get_session)):
    return TaskRepository(session = session)

async def get_task_service (repository: TaskRepository = Depends(get_task_repository)):
    return TaskService(repository = repository)