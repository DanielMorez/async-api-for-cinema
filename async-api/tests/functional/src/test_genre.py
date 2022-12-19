import logging
import pytest
from http import HTTPStatus

from settings import test_settings
from testdata.generate_data.genres import generate_genre, generate_genres
from testdata.parametrize.genre_params import genre_list_params, cache_genre_list_params
from testdata.models.genre import Genre


async def test_genre_by_id(es_write_data, make_get_request):
    logging.info("#1 Generating content")
    genre_es = generate_genre()
    path = f"/api/v1/genres/{genre_es['id']}"
    await es_write_data([genre_es], "genres", "id")
    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(test_settings.service_url, path)
    logging.info("#3 Checking the answers")
    assert response["status"] == HTTPStatus.OK


async def test_genre_validation(es_write_data, make_get_request):
    logging.info("#1 Generating content")
    genre_es = generate_genre()
    genre_model = Genre(**genre_es)
    path = f"/api/v1/genres/{genre_es['id']}"
    await es_write_data([genre_es], "genres", "id")
    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(test_settings.service_url, path)
    logging.info("#3 Checking the answers")
    expected_answer = genre_model.dict()
    assert response["body"] == expected_answer


@pytest.mark.parametrize("query_data, expected_answer", genre_list_params)
async def test_get_list_genre(
    es_write_data, make_get_request, query_data, expected_answer
):
    logging.info("#1 Generating content")
    genre_es = generate_genres(100)
    await es_write_data(genre_es, "genres", "id")
    path = "/api/v1/genres"
    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(test_settings.service_url, path, query_data)
    logging.info("#3 Checking the answers")
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]


@pytest.mark.parametrize("query_data, expected_answer", cache_genre_list_params)
async def test_genres_cache(
    redis_client, es_write_data, make_get_request, query_data, expected_answer
):
    logging.info("#1 Generating content")
    genre_es = generate_genres()
    await es_write_data(genre_es, "genres", "id")
    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(
        test_settings.service_url, "/api/v1/genres", query_data
    )
    logging.info("#3 Get cache from Redis")
    cache_data = await redis_client.get(expected_answer["key"])
    cache_data = eval(cache_data.replace("null", "None"))
    logging.info("#4 Checking the answers")
    assert response["status"] == expected_answer["status"]
    assert response["body"] == cache_data
