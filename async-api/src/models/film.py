from datetime import date
from typing import Optional

from models.base_model import PyBaseModel
from models.constants import FilmWorkType
from models.genre import Genre
from models.person import Person


class Film(PyBaseModel):
    """Описание модели кинопроизведения."""
    title: str
    description: Optional[str]
    type: FilmWorkType = FilmWorkType.MOVIE
    imdb_rating: float = 0.0
    genres: list[Genre] = []
    genres_names: list[str]
    directors: list[Person] = []
    directors_names: list[str]
    actors: list[Person] = []
    actors_names: list[str]
    writers: list[Person] = []
    writers_names: list[str]
