import aiohttp
import logging
import pytest
import json

from pydantic import AnyUrl


@pytest.fixture
def get_token():
    async def inner(service_url: AnyUrl, query_data: dict | None = None):
        session = aiohttp.ClientSession()
        url = service_url + "/api/v1/user/login"
        headers = [("Content-Type", "application/json;")]
        async with session.post(
            url, headers=headers, data=json.dumps(query_data)
        ) as response:
            data = await response.read()
            body = json.loads(data)
            response = {
                "headers": response.headers,
                "status": response.status,
                "body": body,
            }
        await session.close()
        logging.info(f"Got response with code {response['status']}")
        return {
            "access_token": response["body"]["access_token"],
            "refresh_token": response["body"]["refresh_token"],
        }

    return inner


@pytest.fixture
def add_role():
    async def inner(service_url: AnyUrl, token: str, query_data: dict | None = None):
        session = aiohttp.ClientSession()
        url = service_url + "/api/v1/user/roles"
        headers = {
            f"Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        async with session.post(
            url, headers=headers, data=json.dumps({"name": query_data})
        ) as response:
            data = await response.read()
            body = json.loads(data)
            response = {
                "headers": response.headers,
                "status": response.status,
                "body": body,
            }
        await session.close()
        logging.info(f"Got response with code {response['status']}")
        return

    return inner
