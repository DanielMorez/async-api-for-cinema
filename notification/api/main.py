import uvicorn
import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import adapters
from adapters.rabbitmq_producer import RabbitMQProducerClient
from api.v1 import views
from config import settings
from cores.logger import LOGGING

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/notifications/openapi",
    openapi_url="/api/notifications/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    adapters.producer = RabbitMQProducerClient(**settings.rabbitmq.dict())
    await adapters.producer.startup()


@app.on_event("shutdown")
async def shutdown():
    await adapters.producer.shutdown()

app.include_router(views.router, prefix="/notifications")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
