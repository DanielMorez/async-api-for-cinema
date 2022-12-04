from enum import Enum


class FilmWorkType(str, Enum):
    """Варианты типов кинопроизведений."""

    MOVIE = "movie"
    TV_SHOW = "tv_show"
