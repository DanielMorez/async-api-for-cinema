import logging

import uvicorn as uvicorn
from api.v1 import user
from core import config
from core.logger import LOGGING
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.API_VERSION,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(user.user_router, prefix='/api/v1/user', tags=['user'])
app.include_router(user.category_router, prefix='/api/v1/category', tags=['category'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8002,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
