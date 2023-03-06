import uuid
from uuid import UUID

from core.utils import orjson_dumps
from orjson import orjson
from pydantic import BaseModel, Field


class Bookmark(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    user_id: UUID
    film_id: UUID

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
