from enum import Enum

from fastapi import Query
from pydantic import Field, validator

from api.v1.queries_params.base import QueryListBaseModel


class GenreSortTypes(str, Enum):
    NAME_ASC = "name"
    NAME_DESC = "-name"


class GenreListParams(QueryListBaseModel):
    name: str = Query(None, description="Search by names")
    sort: str = Query(
        None,
        regex=f'(None|{"|".join(GenreSortTypes)})',
        description="Sorting by genre name",
    )

    @validator("sort", pre=True, always=True)
    def set_sort(cls, sort):
        if sort == GenreSortTypes.NAME_ASC:
            return sort
        elif sort == GenreSortTypes.NAME_DESC:
            return "name:desc"
