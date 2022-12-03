from fastapi import Query
from fastapi_utils.api_model import APIModel


class QueryListBaseModel(APIModel):
    sort: str = Query(None)
    page_size: int = Query(100)
    page_number: int = Query(0)

    class Config:
        validate_assignment = True
