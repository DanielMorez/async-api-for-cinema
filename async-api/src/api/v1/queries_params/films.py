from enum import Enum

from fastapi import Query
from pydantic import validator, Field

from .base import QueryListBaseModel


class FilmSortTypes(str, Enum):
    RATING_ASC = "imdb_rating"  # imdb_rating:asc
    RATING_DESC = "-imdb_rating"  # imdb_rating:desc


class FilmMixin(QueryListBaseModel):
    sort: str = Field(
        Query(
            "-imdb_rating",
            regex=f'(None|{"|".join(FilmSortTypes)})',
            description="Sorting by IMDB_rating",
        ),
    )

    @validator("sort", pre=True, always=True)
    def set_sort(cls, sort):
        if sort == FilmSortTypes.RATING_ASC:
            return sort
        elif sort == FilmSortTypes.RATING_DESC:
            return "imdb_rating:desc"


class FilmListParams(FilmMixin):
    genre_id: str | None = Field(
        Query(None, alias="filter[genre]", description="Filter by genre UUID")
    )


class FilmQueryParams(FilmMixin):
    query: str | None = Field(Query(None, description="Film searching"))
