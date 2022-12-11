import datetime
import logging
import uuid
import pytest

from settings import test_settings
from testdata.parametrize.films_search import params


@pytest.mark.parametrize(
    'query_data, expected_answer', params
)
async def test_search(es_write_data, make_get_request, query_data, expected_answer):
    logging.info("#1 Generating content")

    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'film_work_type': 'movie'
    } for _ in range(60)]

    await es_write_data(es_data, "movies", "id")

    logging.info("#3 Requesting data from ES via API")

    response = await make_get_request(test_settings.service_url, "/api/v1/films/search", query_data)

    logging.info("#4 Checking the answer")

    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]
