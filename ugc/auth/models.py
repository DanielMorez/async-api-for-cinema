from uuid import UUID

from orjson import orjson
from pydantic import BaseModel, Field
from starlette.authentication import BaseUser

from core.utils import orjson_dumps


class User(BaseModel, BaseUser):
    id: UUID
    login: str | None
    first_name: str | None
    last_name: str | None
    email: str | None
    roles: list[str] = Field([])

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.email or self.login

    @property
    def identity(self) -> str:
        return str(self.id)
