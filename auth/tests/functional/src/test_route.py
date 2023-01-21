from http import HTTPStatus

import pytest

from settings import test_settings
from testdata.parametrize.test_route import (
    test_register_post,
    test_refresh_post,
    test_login_post,
    test_roles_put,
)
from testdata.parametrize.test_route import test_roles_get
from utils.helpers.request_methods import make_post_request, make_get_request, make_put_request, make_delete_request
from plugins.common import add_role

@pytest.mark.order(1)
@pytest.mark.parametrize("query_data, expected_answer", test_register_post)
@pytest.mark.asyncio
async def test_register_post(query_data, expected_answer):
    pytest.status = "First test"
    response = await make_post_request(test_settings.service_url, "/api/v1/user/register", query_data)

    assert response["status"] == HTTPStatus.CREATED
    assert list(response["body"].keys()) == expected_answer["body"]


@pytest.mark.order(2)
@pytest.mark.parametrize("query_data, expected_answer", test_login_post)
@pytest.mark.asyncio
async def test_login_post(query_data, expected_answer):
    response = await make_post_request(test_settings.service_url, "/api/v1/user/login", query_data)

    assert response["status"] == HTTPStatus.OK
    assert list(response["body"].keys()) == expected_answer["body"]


@pytest.mark.order(3)
@pytest.mark.parametrize("query_data, expected_answer", test_refresh_post)
@pytest.mark.asyncio
async def test_refresh_post(get_token, query_data, expected_answer):
    pytest.token = await get_token()
    response = await make_post_request(
        test_settings.service_url,
        "/api/v1/user/token-refresh",
        query_data,
        pytest.token["refresh_token"],
    )

    assert response["status"] == HTTPStatus.OK
    assert list(response["body"].keys()) == expected_answer["body"]


@pytest.mark.order(4)
@pytest.mark.parametrize("query_data, expected_answer", test_roles_get)
@pytest.mark.asyncio
async def test_roles_post(query_data, expected_answer):
    response = await add_role(
        test_settings.service_url, "/api/v1/user/roles", pytest.token["access_token"], query_data["login"]
    )
    assert response["status"] == HTTPStatus.FORBIDDEN


@pytest.mark.order(5)
@pytest.mark.parametrize("query_data, expected_answer", test_roles_get)
@pytest.mark.asyncio
async def test_roles_get(get_token, query_data, expected_answer):
    response = await make_get_request(
        test_settings.service_url,
        "/api/v1/user/roles",
        query_data,
        pytest.token["access_token"],
    )
    assert response["status"] == HTTPStatus.FORBIDDEN


@pytest.mark.order(6)
@pytest.mark.asyncio
async def test_profile_get():
    response = await make_get_request(
        test_settings.service_url,
        "/api/v1/user/profile",
        {},
        pytest.token["access_token"],
    )
    pytest.user_id = response["body"]["id"]
    assert response["status"] == HTTPStatus.OK


@pytest.mark.order(7)
@pytest.mark.asyncio
async def test_login_histories_get():
    response = await make_get_request(
        test_settings.service_url,
        "/api/v1/user/login-histories",
        {},
        pytest.token["access_token"],
    )
    assert response["status"] == HTTPStatus.OK


@pytest.mark.order(8)
@pytest.mark.parametrize("query_data, expected_answer", test_roles_put)
@pytest.mark.asyncio
async def test_roles_put(get_token, query_data, expected_answer):
    response = await make_put_request(
        test_settings.service_url,
        "/api/v1/user/roles",
        query_data,
        pytest.token["access_token"],
    )

    assert response["status"] == HTTPStatus.FORBIDDEN
