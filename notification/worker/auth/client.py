from json import loads
from requests import post
from pydantic import AnyUrl

from auth.models import User


class AuthClient:
    def __init__(self, dsn: AnyUrl):
        self._dsn = dsn

    def get_personal_data_by_ids(self, user_ids: list[str]) -> list[User]:
        response = post(self._dsn + "/api/v1/user/user-data", json={"user_ids": user_ids})
        if response.ok:
            return [User(**user) for user in loads(response.content)]
        return []
