from enum import Enum

from fastapi import Query

from api.v1.queries_params.base import QueryListBaseModel


class GenderTypes(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class PersonSortTypes(str, Enum):
    NAME_ASC = 'name'
    NAME_DESC = 'name:desc'


class PersonListParams(QueryListBaseModel):
    roles: str = Query(None)
    films: str = Query(None)
    name: str = Query(None)
    gender: str = Query(
        None, regex=f'(None|{"|".join(GenderTypes)})'
    )
    sort: str = Query(
        None, regex=f'(None|{"|".join(PersonSortTypes)})'
    )

    @property
    def string_query_params(self):
        return ["roles", "films"]
