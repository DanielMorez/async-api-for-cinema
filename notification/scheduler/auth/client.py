from json import loads
from uuid import UUID
from requests import post
from pydantic import AnyUrl


class AuthClient:
    def __init__(self, dsn: AnyUrl):
        self._dsn = dsn

    def get_users_with_filter(self, filters: dict) -> list[UUID]:
        response = post(self._dsn + "/api/v1/user/user-ids", json=filters)
        if response.ok:
            return loads(response.content)
        return []
