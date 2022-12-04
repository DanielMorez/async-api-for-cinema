from models.base_model import BaseModel


class Genre(BaseModel):
    """Описание модели жанров кинопроизведений."""

    name: str
    description: str | None
