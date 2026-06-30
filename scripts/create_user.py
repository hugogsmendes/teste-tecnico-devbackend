import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.database.db import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.users import User
from src.utils.security import hash_password


async def create_user():
    session: AsyncSession = SessionLocal()
    try:
        new_user = User(
            nome = "UsuarioTeste",
            email = "usuario@teste.com",
            senha_hash = hash_password("usuario123")
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        print(f"Usuário criado com sucesso: {new_user.nome} ({new_user.email})")
    except Exception as e:
        await session.rollback()
        print(f"Erro ao criar usuário: {e}")
        raise
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(create_user())