from enum import Enum

from fastapi import Query

from .base import QueryListBaseModel


class FilmSortTypes(str, Enum):
    RATING_ASC = 'imdb_rating'
    RATING_DESC = 'imdb_rating:desc'


class FilmListParams(QueryListBaseModel):
    title: str = Query(None)
    genres: str = Query(None)
    actors: str = Query(None)
    writers: str = Query(None)
    directors: str = Query(None)
    sort: str = Query(
        FilmSortTypes.RATING_DESC,
        regex=f'({"|".join(FilmSortTypes)})'
    )
    imdb_rating_gt: float = Query(None, gte=0, le=10)
    imdb_rating_lt: float = Query(None, gte=0, le=10)

    @property
    def string_query_params(self):
        return ["title", "actors", "writers", "directors", "genres"]

    @property
    def contains_rating_filter(self) -> bool:
        return self.imdb_rating_gt or self.imdb_rating_lt
