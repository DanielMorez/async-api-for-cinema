from enum import Enum


class FilmWorkType(str, Enum):
    """Варианты типов кинопроизведений."""

    movie = 'movie'
    tv_show = 'tv_show'
