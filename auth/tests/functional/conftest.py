import aiohttp
import logging
import pytest
import json

from pytest_asyncio.plugin import SubRequest

from settings import test_settings
from testdata.parametrize.test_route import login_authorization


@pytest.fixture(params=[{"url": test_settings.service_url, "auth_data": login_authorization}], scope="session")
def get_token(request: SubRequest):
    async def inner():
        session = aiohttp.ClientSession()
        url = request.param["url"] + "/api/v1/user/login"
        headers = [("Content-Type", "application/json;")]
        async with session.post(url, headers=headers, data=json.dumps(request.param["auth_data"])) as response:
            data = await response.read()
            body = json.loads(data)
            response = {
                "headers": response.headers,
                "status": response.status,
                "body": body,
            }
        logging.info(f"Got response with code {response['status']}")
        return {
            "access_token": response["body"]["access_token"],
            "refresh_token": response["body"]["refresh_token"],
        }

    return inner
