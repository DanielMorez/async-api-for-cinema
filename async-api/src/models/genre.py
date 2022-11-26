from models.baseModelConf import PyBaseModel


class Genre(PyBaseModel):
    """Описание модели жанров кинопроизведений."""
    name: str
