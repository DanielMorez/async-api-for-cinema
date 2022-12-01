from typing import Optional

from models.base_model import PyBaseModel


class Person(PyBaseModel):
    """Описание модели персон."""
    name: str
    gender: Optional[str]
    roles_names: list[str]
    films_names: list[str]
