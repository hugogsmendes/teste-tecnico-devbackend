from sqlalchemy.ext.asyncio import AsyncSession

class TaskRepository:

    def __init__(self, session: AsyncSession):
        self.session = session