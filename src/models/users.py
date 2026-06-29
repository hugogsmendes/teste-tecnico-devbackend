from src.database.db import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Text, DateTime, Integer, func
from datetime import datetime


class User (Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    nome: Mapped[str] = mapped_column(Text, nullable = False)
    email: Mapped[str] = mapped_column(Text, nullable = False)
    senha_hash: Mapped[str] = mapped_column(Text, nullable = False)
    data_de_criacao: Mapped[datetime] = mapped_column(DateTime, nullable = False, server_default = func.now())