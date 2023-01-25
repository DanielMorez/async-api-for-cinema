import json
import logging

import aiohttp
from pydantic import AnyUrl


async def make_get_request(
    service_url: AnyUrl,
    endpoint: str,
    query_data: dict | None = None,
    token: str = None,
):
    session = aiohttp.ClientSession()
    url = service_url + endpoint
    if token:
        headers = {f"Authorization": f"Bearer {token}"}
    else:
        headers = [("Content-Type", "application/json;")]
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


async def make_post_request(
    service_url: AnyUrl,
    endpoint: str,
    query_data: dict | None = None,
    token: str = None,
):
    session = aiohttp.ClientSession()
    url = service_url + endpoint
    if token:
        headers = {f"Authorization": f"Bearer {token}"}
    else:
        headers = [("Content-Type", "application/json;")]
    async with session.post(url, headers=headers, data=json.dumps(query_data)) as response:
        data = await response.read()
        body = json.loads(data)
        response = {
            "headers": response.headers,
            "status": response.status,
            "body": body,
        }
    await session.close()
    logging.info(f"Got response with code {response['status']}")
    return response


async def make_put_request(
    service_url: AnyUrl,
    endpoint: str,
    query_data: dict | None = None,
    token: str = None,
):
    session = aiohttp.ClientSession()
    url = service_url + endpoint
    if token:
        headers = {f"Authorization": f"Bearer {token}"}
    else:
        headers = [("Content-Type", "application/json;")]
    async with session.put(url, headers=headers, data=json.dumps(query_data)) as response:
        data = await response.read()
        body = json.loads(data)
        response = {
            "headers": response.headers,
            "status": response.status,
            "body": body,
        }
    await session.close()
    logging.info(f"Got response with code {response['status']}")
    return response


async def make_delete_request(
    service_url: AnyUrl,
    endpoint: str,
    query_data: dict | None = None,
    token: str = None,
):
    session = aiohttp.ClientSession()
    url = service_url + endpoint
    headers = {
        f"Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    async with session.delete(url, headers=headers, data=json.dumps(query_data)) as response:
        data = await response.read()
        body = json.loads(data)
        response = {
            "headers": response.headers,
            "status": response.status,
            "body": body,
        }
    await session.close()
    logging.info(f"Got response with code {response['status']}")
    return response
