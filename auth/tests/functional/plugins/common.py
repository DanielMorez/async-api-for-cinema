import json
import logging

import aiohttp
from pydantic import AnyUrl


async def add_role(
    service_url: AnyUrl, endpoint: str, token: str, query_data: dict | None = None
):
    session = aiohttp.ClientSession()
    url = service_url + endpoint
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
    return response
