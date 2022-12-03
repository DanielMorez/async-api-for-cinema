import uuid
from datetime import datetime

from pydantic import BaseModel


class Film(BaseModel):
    id: uuid.UUID
    title: str


class Person(BaseModel):
    id: uuid.UUID
    name: str
    gender: str | None
    roles: list[str]
    films: list[Film]
    modified: datetime

    class Config:
        validate_assignment = True
