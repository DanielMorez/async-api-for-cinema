from pydantic import BaseModel


class Film(BaseModel):
    id: str
    title: str


class Person(BaseModel):
    """Описание модели персон."""
    id: str
    name: str
    gender: str | None
    roles_names: list[str]
    films: list[Film]
