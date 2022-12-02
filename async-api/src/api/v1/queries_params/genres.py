from enum import Enum

from fastapi import Query

from api.v1.queries_params.base import QueryListBaseModel


class GenreSortTypes(str, Enum):
    NAME_ASC = 'name'
    NAME_DESC = 'name:desc'


class GenreListParams(QueryListBaseModel):
    name: str = Query(None)
    sort: str = Query(
        None, regex=f'(None|{"|".join(GenreSortTypes)})'
    )

    @property
    def string_query_params(self):
        return ["name"]