import json
import logging

import aiohttp
import pytest
from multidict import CIMultiDictProxy
from pydantic import AnyUrl


@pytest.fixture
def make_get_request():
    async def inner(service_url: AnyUrl, endpoint: str,
                    query_data: dict | None = None,
                    token: str = None,
                    ):
        session = aiohttp.ClientSession()
        url = service_url + endpoint
        if token:
            headers = {f'Authorization': f'Bearer {token}'}
        else:
            headers = [('Content-Type', 'application/json;')]
        async with session.get(url, headers=headers, data=json.dumps(query_data)) as response:
            body = await response.json()
            response = {
                "headers": response.headers,
                "status": response.status,
                "body": body,
            }
        await session.close()
        logging.info(f"Got response with code {response['status']}")
        return response

    return inner


@pytest.fixture
def make_post_request():
    async def inner(service_url: AnyUrl, endpoint: str,
                    query_data: dict | None = None,
                    token: str = None):
        session = aiohttp.ClientSession()
        url = service_url + endpoint
        if token:
            headers = {f'Authorization': f'Bearer {token}'}
        else:
            headers = [('Content-Type', 'application/json;')]
        async with session.post(url, headers=headers, data=json.dumps(query_data)) as response:
            data = await response.read()
            body = json.loads(data)
            response = {
                "headers": response.headers,
                "status": response.status,
                "body": body
            }
        await session.close()
        logging.info(f"Got response with code {response['status']}")
        return response

    return inner
