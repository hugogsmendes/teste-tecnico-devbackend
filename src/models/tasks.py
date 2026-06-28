from src.database.db import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Enum, Text, DateTime, Integer, func
import enum
from datetime import datetime


class Task (Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    titulo: Mapped[str] = mapped_column(Text, nullable = False)
    descricao: Mapped[str] = mapped_column(Text, nullable = False)
    status: Mapped[enum.Enum] = mapped_column(Enum("Pendente", "Em andamento", "Concluída", name = "StatusTarefa"), 
                                              nullable = False)
    data_de_criacao: Mapped[datetime] = mapped_column(DateTime, nullable = False, server_default = func.now())
    data_de_atualizacao: Mapped[datetime] = mapped_column(DateTime, nullable = True, onupdate = func.now())
    data_de_exclusao: Mapped[datetime] = mapped_column(DateTime, nullable = True)