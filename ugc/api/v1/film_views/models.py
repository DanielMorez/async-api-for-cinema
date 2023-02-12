from uuid import UUID

from orjson import orjson
from pydantic import BaseModel

from core.utils import orjson_dumps


class Frame(BaseModel):
    user_id: UUID
    film_id: UUID
    timestamp: int

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
