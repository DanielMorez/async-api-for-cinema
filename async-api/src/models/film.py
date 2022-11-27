from datetime import date

from models.base_model import PyBaseModel
from models.constants import FilmWorkType


class Film(PyBaseModel):
    """Описание модели кинопроизведения."""
    title: str
    description: str
    type: FilmWorkType = FilmWorkType.movie
    creation_date: date
    rating: float = 0.0
    age_classification: int = 0
    by_subscription: bool = False
    genres: list[str] = []
    directors: list[str] = []
    actors: list[str] = []
    writers: list[str] = []
    producers: list[str] = []
