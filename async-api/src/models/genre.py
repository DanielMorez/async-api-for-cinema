from typing import Optional

from models.base_model import PyBaseModel


class Genre(PyBaseModel):
    """Описание модели жанров кинопроизведений."""
    name: str
    description: Optional[str]
