import uuid

from uuid import UUID

from bson import ObjectId as BsonObjectId

from core.utils import orjson_dumps
from orjson import orjson
from pydantic import BaseModel, Field


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string", example="")


class Rate(BaseModel):
    id: PydanticObjectId = Field(None, alias="_id")
    user_id: UUID
    film_id: UUID
    stars: int = Field(None, ge=0, le=10)

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UserFilmRating(BaseModel):
    id: PydanticObjectId = Field(None, alias="_id")
    film_id: UUID
    stars_avg: float = Field(None, ge=0, le=10)
    count: int = Field(0)
    stars: int = Field(None)

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
