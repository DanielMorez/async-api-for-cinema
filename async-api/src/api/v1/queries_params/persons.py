from enum import Enum

from fastapi import Query
from pydantic import Field

from api.v1.queries_params.base import QueryListBaseModel


class GenderTypes(str, Enum):
    MALE = "male"
    FEMALE = "female"


class PersonSortTypes(str, Enum):
    NAME_ASC = "name"
    NAME_DESC = "name:desc"


class PersonSearchParams(QueryListBaseModel):
    query: str | None = Field(Query(None, description="Person searching"))
