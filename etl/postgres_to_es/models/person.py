from datetime import datetime

from models.movie import NameObject, Movie


class Person(NameObject):
    gender: str | None
    roles: list[str]
    films: list[Movie]

    class Config:
        validate_assignment = True
