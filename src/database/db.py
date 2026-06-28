from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.core.config import Settings

settings = Settings()

DATABASE_URL = settings.DATABASE_URL

# Motor assincrono com BD Postegres
engine = create_async_engine(DATABASE_URL,
                             pool_pre_ping = True,
                             echo = False,
                             pool_size = 5,
                             max_overflow = 15)

class Base (DeclarativeBase):

    """
    Modelo Base para todos os ORMs SqlAlchemy
    """
    pass


SessionLocal = async_sessionmaker(bind = engine,
                                  class_= AsyncSession, 
                                  expire_on_commit = False,
                                  autocommit = False,
                                  autoflush = False)  