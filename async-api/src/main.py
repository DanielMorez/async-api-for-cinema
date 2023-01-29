import logging

import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from api.v1 import films, persons, genres
from constants.documentations import description, tags_metadata
from core.config import Settings
from core.logger import LOGGING
from db import elastic
from db import redis
from helpers.cache_key_builder import key_builder
from middlewares.authentication import CustomAuthBackend

settings = Settings()

app = FastAPI(
    title=settings.project_name,
    description=description,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    openapi_tags=tags_metadata,
    middleware=[Middleware(AuthenticationMiddleware, backend=CustomAuthBackend())]
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.from_url(
        settings.redis_dsn, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(
        RedisBackend(redis.redis),
        prefix="fastapi-cache",
        expire=settings.cache_expire_in_seconds,
        key_builder=key_builder,
    )
    elastic.es = AsyncElasticsearch(hosts=[settings.es_dsn])


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films")
app.include_router(persons.router, prefix="/api/v1/persons")
app.include_router(genres.router, prefix="/api/v1/genres")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
