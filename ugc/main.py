import uvicorn
import logging
from adapters import broker

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from adapters.broker import KafkaProducerClient
from api.v1 import film_views

from core.logger import LOGGING
from core.config import settings
from auth.middlewares import CustomAuthBackend
from openapi.tags import tags_metadata, description

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
    broker.producer = KafkaProducerClient(
        f"{settings.broker.host}:{settings.broker.port}"
    )
    await broker.producer.startup()


@app.on_event("shutdown")
async def shutdown():
    await broker.producer.shutdown()


app.include_router(film_views.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
