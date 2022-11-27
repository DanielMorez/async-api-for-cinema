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
    creation_date: date
    imdb_rating: float = 0.0
    genres: list[Genre] = []
    directors: list[Person] = []
    actors: list[Person] = []
    writers: list[Person] = []
