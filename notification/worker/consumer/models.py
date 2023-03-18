from typing import Any
from uuid import UUID

from orjson import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default) -> str:
    return orjson.dumps(v, default=default).decode()


class Notification(BaseModel):
    type: str = Field(regex="(send_immediately|regular_mailing)")
    template_id: int = Field(default=1)  # Set default template ID
    user_ids: list[UUID]
    context: dict[str, Any]  # There are can be any text

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
