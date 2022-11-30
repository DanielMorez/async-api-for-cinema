from models.base_model import PyBaseModel


class Person(PyBaseModel):
    """Описание модели персон."""
    name: str
