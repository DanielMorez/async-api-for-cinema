import asyncio

import aiohttp
import pytest
import logging

import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from pydantic import AnyUrl

from settings import test_settings
from utils.bulk_query import get_es_bulk_query


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def es_client(event_loop):
    client = AsyncElasticsearch(hosts=test_settings.es_dsn)
    logging.info("Created elasticsearch client.")
    yield client
    logging.info("Closed elasticsearch client.")
    await client.close()


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict], index: str, field: str):
        bulk_query = get_es_bulk_query(data, index, field)
        str_query = "\n".join(bulk_query) + "\n"
        response = await es_client.bulk(operations=str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")
        logging.info(f"Loaded data to elasticsearch for index `{index}`")
    return inner


@pytest.fixture
def make_get_request():
    async def inner(service_url: AnyUrl, endpoint: str, query_data: dict):
        session = aiohttp.ClientSession()
        url = service_url + endpoint
        async with session.get(url, params=query_data) as response:
            body = await response.json()
            response = {
                "headers": response.headers,
                "status": response.status,
                "body": body
            }
        await session.close()
        logging.info(f"Got response with code {response['status']}")
        return response
    return inner