import logging

from motor.motor_asyncio import AsyncIOMotorClient

import adapters
import sentry_sdk
import uvicorn
from adapters.broker import KafkaProducerClient
from db import mongo
from api.v1 import film_views, bookmarks
from api.v1.rating.views import router as rating_routes
from api.v1.reviews.views import router as reviews_routes
from core.config import settings
from core.logger import LOGGING
from core.logstash import init_logstash
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from openapi.tags import description, tags_metadata
from sentry_sdk.integrations.fastapi import FastApiIntegration
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from auth.middlewares import CustomAuthBackend

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[FastApiIntegration()],
        traces_sample_rate=1.0
    )

if settings.logstash_enable:
    init_logstash(settings.logstash)

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
    mongo.mongo = AsyncIOMotorClient(
        settings.mongo_dsn,
        uuidRepresentation='standard'
    )
    adapters.producer = KafkaProducerClient(
        f"{settings.broker.host}:{settings.broker.port}"
    )
    await adapters.producer.startup()


@app.on_event("shutdown")
async def shutdown():
    await mongo.mongo.close()
    await adapters.producer.shutdown()

app.include_router(film_views.router)
app.include_router(bookmarks.router)
app.include_router(rating_routes)
app.include_router(reviews_routes)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
