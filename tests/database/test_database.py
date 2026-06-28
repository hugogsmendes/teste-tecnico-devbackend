import asyncio
from sqlalchemy import text
from src.database.db import engine


def test_connect():
    async def run_check():
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            assert result.scalar_one() == 1

        await engine.dispose()

    asyncio.run(run_check())

