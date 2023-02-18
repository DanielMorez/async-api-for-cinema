import adapters
from contextvars import ContextVar
import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
import uvicorn

sentry_sdk.init(
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)

from adapters.broker import KafkaProducerClient
from api.v1 import film_views

from core.logger import LOGGING
from core.config import settings
from auth.middlewares import CustomAuthBackend
from openapi.tags import tags_metadata, description


x_request_id: ContextVar[str] = ContextVar('x_request_id', default='')

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = x_request_id.get()
        return True


logstash_handler = AsynchronousLogstashHandler(
    settings.logstash.host, 
    settings.logstash.port, 
    None,
    transport='logstash_async.transport.UdpTransport'
)
logstash_handler.formatter = LogstashFormatter(tags=['ugc'])
logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(logstash_handler)
logging.getLogger().addFilter(RequestIdFilter())

app = FastAPI(
    title=settings.project_name,
    description=description,
    docs_url="/api/ugc/openapi",
    openapi_url="/api/ugc/openapi.json",
    default_response_class=ORJSONResponse,
    openapi_tags=tags_metadata,
    middleware=[
        Middleware(AuthenticationMiddleware, backend=CustomAuthBackend()),
    ],
)


@app.on_event("startup")
async def startup():
    adapters.producer = KafkaProducerClient(
        f"{settings.broker.host}:{settings.broker.port}"
    )
    await adapters.producer.startup()


@app.on_event("shutdown")
async def shutdown():
    await adapters.producer.shutdown()


app.include_router(film_views.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
