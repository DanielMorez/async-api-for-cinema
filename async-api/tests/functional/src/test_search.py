import json
import logging

import pytest

from settings import test_settings
from testdata.generate_data.search import (
    generate_search_films,
    extract_es_index,
    generate_persons_films,
)
from testdata.models.film import Film, SearchPerson
from testdata.parametrize.films_search import (
    films_search,
    cache_search_films,
    persons_search,
    cache_search_persons,
)


@pytest.mark.parametrize("query_data, expected_answer", films_search)
async def test_films_search(
    es_write_data, make_get_request, query_data, expected_answer
):
    logging.info("#1 Generating content")
    es_data = generate_search_films(60)
    await es_write_data(es_data, "movies", "id")

    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(
        test_settings.service_url, "/api/v1/films/search", query_data
    )

    logging.info("#3 Checking the answers")
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]


async def test_films_search_validation(es_write_data, make_get_request, get_index_es):
    logging.info("#1 Create data to ES")
    es_data = generate_search_films(60)
    await es_write_data(es_data, "movies", "id")

    logging.info("#2 Get data from ES")
    es_data = await get_index_es("movies", "imdb_rating:desc")

    logging.info("#3 Extract data to list")
    search_list = extract_es_index(es_data)

    logging.info("#4 Convert list to Search_films object")
    search_films = [Film(**film).dict() for film in search_list]

    logging.info("#5 Requesting data from ES via API")
    path = "/api/v1/films/search"
    response = await make_get_request(test_settings.service_url, path)
    logging.info("#6 Checking the answer")
    assert response["body"] == search_films


@pytest.mark.parametrize("query_data, expected_answer", cache_search_films)
async def test_film_cache(
    redis_client, es_write_data, make_get_request, query_data, expected_answer
):
    logging.info("#1 Generating content")
    es_data = generate_search_films()
    await es_write_data(es_data, "movies", "id")

    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(
        test_settings.service_url, "/api/v1/films/search", query_data
    )

    logging.info("#3 Get cache from Redis")
    cache_data = await redis_client.get(expected_answer["key"])

    logging.info("#3 Convert cache from str to list")
    cache_data = json.loads(cache_data)

    logging.info("#4 Checking the answers")
    assert response["status"] == expected_answer["status"]
    assert cache_data


@pytest.mark.parametrize("query_data, expected_answer", persons_search)
async def test_persons_search(
    es_write_data, make_get_request, query_data, expected_answer
):
    logging.info("#1 Generating content")
    es_data = generate_persons_films()
    await es_write_data(es_data, "persons", "id")

    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(
        test_settings.service_url, "/api/v1/persons/search", query_data
    )

    logging.info("#3 Checking the answers")
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]


async def test_persons_search_validation(es_write_data, make_get_request, get_index_es):
    logging.info("#1 Create data to ES")
    es_data = generate_persons_films()
    await es_write_data(es_data, "persons", "id")

    logging.info("#2 Get data from ES")
    es_data = await get_index_es("persons", "_score")

    logging.info("#3 Extract data to list")
    search_list = extract_es_index(es_data)

    logging.info("#4 Convert list to Search_films object")
    search_persons = [SearchPerson(**person).dict() for person in search_list]

    logging.info("#5 Requesting data from ES via API")
    path = "/api/v1/persons/search"
    response = await make_get_request(test_settings.service_url, path)

    logging.info("#6 Checking the answer")
    assert response["body"] == search_persons


@pytest.mark.parametrize("query_data, expected_answer", cache_search_persons)
async def test_persons_cache(
    redis_client, es_write_data, make_get_request, query_data, expected_answer
):
    logging.info("#1 Generating content")
    es_data = generate_persons_films()
    await es_write_data(es_data, "persons", "id")

    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(
        test_settings.service_url, "/api/v1/persons/search", query_data
    )

    logging.info("#3 Get cache from Redis")
    cache_data = await redis_client.get(expected_answer["key"])

    logging.info("#3 Convert cache from str to list")
    cache_data = eval(cache_data.replace("null", "None"))

    logging.info("#4 Checking the answers")
    assert response["status"] == expected_answer["status"]
    assert cache_data
