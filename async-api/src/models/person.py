from datetime import date
from typing import Optional
from uuid import UUID

from models.base_model import PyBaseModel
from models.film import Film

class Person(PyBaseModel):
    """Описание модели персон."""
    first_name: str
    last_name: str
    film_ids: list[Film]
    role: Optional[list[str]]
