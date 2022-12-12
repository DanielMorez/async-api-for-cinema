import asyncio
import datetime
import logging
import uuid
import pytest

from settings import test_settings
from testdata.parametrize.person_data import params


@pytest.mark.parametrize(
    "query_data, expected_answer", params
)
async def test_persons_search(es_write_data, make_get_request, query_data, expected_answer):
    async def search_persons():
        # подождем немного пока база заполнится данными
        await asyncio.sleep(3)

        response = await make_get_request(test_settings.service_url, "/api/v1/persons/search", query_data)

        logging.info("#4 Checking the answer")

        assert response["status"] == expected_answer["status"]
        assert len(response["body"]) == expected_answer["length"]

    async def persons_id_film(person_id: str):
        # подождем немного пока база заполнится данными
        await asyncio.sleep(5)

        response = await make_get_request(test_settings.service_url, f"/api/v1/persons/{person_id}/film", None)

        logging.info("#4 Checking the answer")

        assert response["status"] == expected_answer["status"]
    #    assert len(response["body"]) == expected_answer["length"]

    async def persons_id(person_id: str):
        # подождем немного пока база заполнится данными
        await asyncio.sleep(5)

        response = await make_get_request(test_settings.service_url, f"/api/v1/persons/{person_id}", None)

        logging.info("#4 Checking the answer")

        assert response["status"] == expected_answer["status"]
      #  assert len(response["body"]) == expected_answer["length"]

    logging.info("#1 Generating content")

    es_data = [{
        "id": str(uuid.uuid4()),
        "name": "Annabeth",
        "gender": "female",
        "roles_names": ["actor", "producer"],
        "films_names": ["The Star", "NeverLand"],
        "films": [
            {"id": "111", "title": "The Star"},
            {"id": "222", "title": "NeverLand"}
        ],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    } for _ in range(50)]
    person_id = es_data[0]["id"]

    await es_write_data(es_data, "persons", "id")
    logging.info("#3 Requesting data from ES via API")

    await search_persons()
    await persons_id_film(person_id)
    await persons_id(person_id)
