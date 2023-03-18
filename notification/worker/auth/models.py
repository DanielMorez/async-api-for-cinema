from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    login: str
    first_name: str | None
    last_name: str | None
    email: str
