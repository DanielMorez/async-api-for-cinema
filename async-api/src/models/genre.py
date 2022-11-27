from models.base_model import PyBaseModel


class Genre(PyBaseModel):
    """Описание модели жанров кинопроизведений."""
    name: str
