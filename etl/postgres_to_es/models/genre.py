import uuid

from datetime import datetime
from pydantic import BaseModel, validator


class Genre(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    modified: datetime

    class Config:
        validate_assignment = True

    @validator('description', pre=True, always=True)
    def set_description(cls, description):
        return description or ''
