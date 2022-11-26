from datetime import date
from typing import Optional
from uuid import UUID

from models.baseModelConf import PyBaseModel


class Person(PyBaseModel):
    """Описание модели персон."""
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    actor: list[UUID] = []
    director: list[UUID] = []
    writer: list[UUID] = []
    producer: list[UUID] = []
