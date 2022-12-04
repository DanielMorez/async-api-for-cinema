from fastapi import Query
from fastapi_utils.api_model import APIModel
from pydantic import Field, validator


class QueryListBaseModel(APIModel):
    page_size: int | None = Field(
        Query(50, alias="page[size]", description="Items amount on page", ge=1)
    )
    page_number: int | None = Field(
        Query(1, alias="page[number]", description="Page number for pagination", ge=1)
    )

    class Config:
        validate_assignment = True

    @validator("page_number", pre=True, always=True)
    def set_page_number(cls, page_number):
        return page_number - 1
