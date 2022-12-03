import uuid

from datetime import datetime
from pydantic import BaseModel, validator


class NameObject(BaseModel):
    id: uuid.UUID
    name: str


class Movie(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    rating: float | None
    type: str | None
    created: datetime
    modified: datetime
    actors: list[NameObject]
    writers: list[NameObject]
    directors: list[NameObject]
    genres: list[NameObject]

    class Config:
        validate_assignment = True

    @validator('description', pre=True, always=True)
    def set_description(cls, description):
        return description or ''
