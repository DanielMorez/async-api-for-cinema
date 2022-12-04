from models.base_model import BaseModel


class Film(BaseModel):
    title: str


class Person(BaseModel):
    """Описание модели персон."""

    name: str
    gender: str | None
    roles_names: list[str]
    films: list[Film]
