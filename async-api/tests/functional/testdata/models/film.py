from pydantic import BaseModel


class Genre(BaseModel):
    """Описание модели жанр."""
    id: str
    name: str


class Person(BaseModel):
    """Описание модели персон."""
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float | None
    title: str
    description: str | None
    genres: list[Genre] = []
    directors: list[Person] = []
    actors: list[Person] = []
    writers: list[Person] = []
    type: str


class SearchPerson(BaseModel):
    id: str
    name: str
    gender: str | None
    roles_names: list = []
    films: list = []
