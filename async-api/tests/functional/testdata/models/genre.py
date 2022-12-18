from pydantic import BaseModel


class Genre(BaseModel):
    """Описание модели жанр."""
    id: str
    name: str
