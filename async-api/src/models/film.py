from models.base_model import BaseModel
from models.constants import FilmWorkType
from models.genre import Genre


class Person(BaseModel):
    name: str


class Film(BaseModel):
    """Описание модели кинопроизведения."""

    title: str
    description: str | None
    type: FilmWorkType = FilmWorkType.MOVIE
    imdb_rating: float | None
    genres: list[Genre] = []
    directors: list[Person] = []
    actors: list[Person] = []
    writers: list[Person] = []
