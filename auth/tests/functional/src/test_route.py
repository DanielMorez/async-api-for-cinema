from http import HTTPStatus

import pytest
from settings import test_settings
from testdata.parametrize.test_route import (
    test_register_post,
    test_refresh_post,
    test_login_post,
)
from testdata.parametrize.test_route import test_roles_get


@pytest.mark.parametrize("query_data, expected_answer", test_register_post)
@pytest.mark.asyncio
async def test_register_post(make_post_request, query_data, expected_answer):
    response = await make_post_request(
        test_settings.service_url, "/api/v1/user/register", query_data
    )

    assert response["status"] == HTTPStatus.CREATED
    assert list(response["body"].keys()) == expected_answer["body"]


@pytest.mark.parametrize("query_data, expected_answer", test_refresh_post)
@pytest.mark.asyncio
async def test_refresh_post(get_token, make_post_request, query_data, expected_answer):
    token = await get_token(test_settings.service_url, query_data)
    response = await make_post_request(
        test_settings.service_url,
        "/api/v1/user/token-refresh",
        query_data,
        token["refresh_token"],
    )

    assert response["status"] == HTTPStatus.OK
    assert list(response["body"].keys()) == expected_answer["body"]


@pytest.mark.parametrize("query_data, expected_answer", test_login_post)
@pytest.mark.asyncio
async def test_login_post(make_post_request, query_data, expected_answer):
    response = await make_post_request(
        test_settings.service_url, "/api/v1/user/login", query_data
    )

    assert response["status"] == HTTPStatus.OK
    assert list(response["body"].keys()) == expected_answer["body"]


@pytest.mark.parametrize("query_data, expected_answer", test_roles_get)
@pytest.mark.asyncio
async def test_roles_get(
    get_token, add_role, make_get_request, query_data, expected_answer
):
    token = await get_token(test_settings.service_url, query_data)
    add_role = await add_role(
        test_settings.service_url, token["access_token"], query_data["login"]
    )
    response = await make_get_request(
        test_settings.service_url,
        "/api/v1/user/roles",
        query_data,
        token["access_token"],
    )
    assert response["status"] == HTTPStatus.OK
