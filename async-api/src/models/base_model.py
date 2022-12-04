import orjson
from pydantic import BaseModel as PydanticBaseModel


def orjson_dumps(v, *, default) -> str:
    return orjson.dumps(v, default=default).decode()


class BaseModel(PydanticBaseModel):
    """Базовая модель для всех моделей."""

    id: str

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
