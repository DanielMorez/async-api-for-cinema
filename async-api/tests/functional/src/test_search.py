import asyncio
import datetime
import logging
import uuid
from pprint import pprint

import pytest

from settings import test_settings
from testdata.generate_data.search import generate_search_film, extract_es_index
from testdata.models.film import Search_film
from testdata.parametrize.films_search import params, cache_search_params


@pytest.mark.parametrize(
    'query_data, expected_answer', params
)
async def test_films_search(es_write_data, make_get_request, query_data, expected_answer):
    logging.info("#1 Generating content")
    es_data = generate_search_film(60)
    await es_write_data(es_data, "movies", "id")

    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(test_settings.service_url, "/api/v1/films/search", query_data)

    logging.info("#3 Checking the answer")
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]


async def test_films_search_validation(es_write_data, make_get_request, get_index_es):
    logging.info("#1 Get data from ES")
    es_data = await get_index_es("movies")

    logging.info("#2 Extract data to list")
    search_list = extract_es_index(es_data)

    logging.info("#3 Convert list to Search_films object")
    search_films = [Search_film(**film) for film in search_list]

    logging.info("#4 Requesting data from ES via API")
    path = "/api/v1/films/search"
    response = await make_get_request(test_settings.service_url, path)

    logging.info("#5 Checking the answer")
    assert response["body"] == search_films


@pytest.mark.parametrize(
    'query_data, expected_answer', cache_search_params
)
async def test_film_cache(redis_client, es_write_data, make_get_request, query_data, expected_answer):
    es_data = generate_search_film()
    await es_write_data(es_data, "movies", "id")

    response = await make_get_request(test_settings.service_url, "/api/v1/films/search", query_data)
    cache_data = await redis_client.get(expected_answer["key"])
    cache_data = eval(cache_data.replace('null', 'None'))
    assert response["status"] == expected_answer["status"]
    assert response["body"][0] == cache_data[0]
