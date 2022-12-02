from models.base_model import BaseModel


class Person(BaseModel):
    """Описание модели персон."""
    name: str
    gender: str
    roles_names: list[str]
    films_names: list[str]


