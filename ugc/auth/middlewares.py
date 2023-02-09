import aiohttp

from http import HTTPStatus
from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials
)

from core.config import settings
from auth.models import User


class CustomAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return AuthCredentials(["not authenticated"]), None

        async with aiohttp.ClientSession() as session:
            async with session.get(
                settings.auth_dsn + "/api/v1/user/profile", headers=conn.headers
            ) as resp:
                if resp.status == HTTPStatus.OK:
                    data = await resp.json()
                    return AuthCredentials(["authenticated"]), User(**data)

        return AuthCredentials(["not authenticated"]), None
