from http import HTTPStatus

import aiohttp

from starlette.authentication import AuthenticationBackend, AuthCredentials

from core.config import Settings
from models.user import User


setting = Settings()


class CustomAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(setting.auth_dsn + "/api/v1/user/profile", headers=conn.headers) as resp:
                if resp.status == HTTPStatus.OK:
                    data = await resp.json()
                    return AuthCredentials(["authenticated"]), User(**data)
