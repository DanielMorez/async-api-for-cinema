from typing import Any
from uuid import UUID

from fastapi import Body
from orjson import orjson
from pydantic import BaseModel

from cores.serializers import orjson_dumps


class Notification(BaseModel):
    type: str = Body(regex="(send_immediately|regular_mailing)")
    template_id: UUID = Body(None)  # Set default template ID
    user_ids: list[UUID]
    context: dict[str, Any]  # There are can be any text

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
