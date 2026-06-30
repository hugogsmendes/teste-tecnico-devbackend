from sqlalchemy.ext.asyncio import AsyncSession
from src.models.users import User
from sqlalchemy import select

class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email (self, email: str) -> User:

        stmt = select(User).filter(User.email == email)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()