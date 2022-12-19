import json
import logging
import pytest
from http import HTTPStatus

from settings import test_settings
from testdata.generate_data.persons import generate_person, generate_persons
from testdata.parametrize.person_params import (
    person_list_params,
    cache_person_list_params,
)
from testdata.models.person import Person


async def test_person_by_id(es_write_data, make_get_request):
    logging.info("#1 Generating content")
    person_es = generate_person()
    path = f"/api/v1/persons/{person_es['id']}"
    await es_write_data([person_es], "persons", "id")
    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(test_settings.service_url, path)
    logging.info("#3 Checking the answers")
    assert response["status"] == HTTPStatus.OK


async def test_person_validation(es_write_data, make_get_request):
    logging.info("#1 Generating content")
    person_es = generate_person()
    person_model = Person(**person_es)
    path = f"/api/v1/persons/{person_es['id']}"
    await es_write_data([person_es], "persons", "id")
    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(test_settings.service_url, path)
    logging.info("#3 Checking the answers")
    expected_answer = person_model.dict()
    assert response["body"] == expected_answer


@pytest.mark.parametrize("query_data, expected_answer", person_list_params)
async def test_get_list_person(
    es_write_data, make_get_request, query_data, expected_answer
):
    logging.info("#1 Generating content")
    person_es = generate_persons(100)
    await es_write_data(person_es, "persons", "id")
    path = "/api/v1/persons/search"
    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(test_settings.service_url, path, query_data)
    logging.info("#3 Checking the answers")
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]


async def test_get_person_film(es_write_data, make_get_request):
    logging.info("#1 Generating content")
    person_es = generate_person()
    path = f"/api/v1/persons/{person_es['id']}/film"
    await es_write_data([person_es], "persons", "id")
    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(test_settings.service_url, path)
    logging.info("#3 Checking the answers")
    assert response["status"] == HTTPStatus.OK


@pytest.mark.parametrize("query_data, expected_answer", cache_person_list_params)
async def test_persons_cache(
    redis_client, es_write_data, make_get_request, query_data, expected_answer
):
    logging.info("#1 Generating content")
    person_es = generate_persons()
    await es_write_data(person_es, "persons", "id")
    logging.info("#2 Requesting data from ES via API")
    response = await make_get_request(
        test_settings.service_url, "/api/v1/persons/search", query_data
    )
    logging.info("#3 Get cache from Redis")
    cache_data = await redis_client.get(expected_answer["key"])
    cache_data = json.loads(cache_data)

    logging.info("#4 Checking the answers")
    assert response["status"] == expected_answer["status"]
    assert cache_data
