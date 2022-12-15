from pydantic import BaseModel


class Genre(BaseModel):
    id: str
    name: str


class Person(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    title: str
    description: str | None
    type: str
    imdb_rating: float | None
    genres: list[Genre] = []
    directors: list[Person] = []
    actors: list[Person] = []
    writers: list[Person] = []
