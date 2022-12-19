import pytest
from http import HTTPStatus

from settings import test_settings
from testdata.generate_data.films import generate_films, generate_film
from testdata.models.film import Film
from testdata.parametrize.film_list import film_list_params, cache_film_list_params


async def test_film_by_id(es_write_data, make_get_request):
    film_es = generate_film()
    path = f"/api/v1/films/{film_es['id']}"
    await es_write_data([film_es], "movies", "id")
    response = await make_get_request(test_settings.service_url, path)

    assert response["status"] == HTTPStatus.OK


async def test_film_validation(es_write_data, make_get_request):
    film_es = generate_film()
    film_model = Film(**film_es)
    path = f"/api/v1/films/{film_es['id']}"
    await es_write_data([film_es], "movies", "id")
    response = await make_get_request(test_settings.service_url, path)
    expected_answer = film_model.dict()

    assert response["body"] == expected_answer


@pytest.mark.parametrize("query_data, expected_answer", film_list_params)
async def test_get_list_film(
    es_write_data, make_get_request, query_data, expected_answer
):
    films = generate_films(100)
    await es_write_data(films, "movies", "id")

    response = await make_get_request(
        test_settings.service_url, "/api/v1/films", query_data
    )

    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]


@pytest.mark.parametrize("query_data, expected_answer", cache_film_list_params)
async def test_film_cache(
    redis_client, es_write_data, make_get_request, query_data, expected_answer
):
    films = generate_films()
    await es_write_data(films, "movies", "id")

    response = await make_get_request(
        test_settings.service_url, "/api/v1/films", query_data
    )
    cache_data = await redis_client.get(expected_answer["key"])

    assert response["status"] == expected_answer["status"]
    assert cache_data
