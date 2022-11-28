import logging

import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films
from core.config import Settings
from core.logger import LOGGING
from db import elastic
from db import redis

settings = Settings()

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.from_url(
        settings.redis_dsn, encoding='utf-8'
    )
    elastic.es = AsyncElasticsearch(hosts=[settings.es_dsn])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
