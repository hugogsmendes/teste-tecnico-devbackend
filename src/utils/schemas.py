from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict

class StatusTarefa(str, Enum):
    pendente = "Pendente"
    em_andamento = "Em andamento"
    concluida = "Concluída"

class ResponseMensagemErro (BaseModel):

    detail: str

class CriarTarefa (BaseModel):

    model_config = ConfigDict(from_attributes = True)

    titulo: str
    descricao: str
    status: StatusTarefa

class AtualizarTarefa (BaseModel):

    model_config = ConfigDict(from_attributes = True)

    titulo: str | None = None
    descricao: str | None = None
    status: StatusTarefa | None = None
class ResponseTarefa (BaseModel):

    model_config = ConfigDict(from_attributes = True)

    id: int
    titulo: str
    descricao: str
    status: StatusTarefa
    data_de_criacao: datetime