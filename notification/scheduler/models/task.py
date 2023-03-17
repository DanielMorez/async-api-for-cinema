from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class Task(BaseModel):
    id: UUID | str
    title: str
    status: str
    context: dict
    scheduled_datetime: datetime | None
    created_at: datetime
    updated_at: datetime
    type: str
    crontab: dict | None
    template_id: int


class Notification(BaseModel):
    type: str
    template_id: int
    user_ids: list[UUID]
    context: dict[str, Any]
