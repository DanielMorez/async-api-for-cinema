from contextvars import ContextVar
from http import HTTPStatus

import aiohttp

from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials
)
from starlette.middleware.base import BaseHTTPMiddleware

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


x_request_id: ContextVar[str] = ContextVar('x_request_id', default='')

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get('X-Request-Id')
        x_request_id.set(request_id)
        return await call_next(request)