from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware


x_request_id: ContextVar[str] = ContextVar('x_request_id', default='')


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get('X-Request-Id')
        x_request_id.set(request_id)
        return await call_next(request)

