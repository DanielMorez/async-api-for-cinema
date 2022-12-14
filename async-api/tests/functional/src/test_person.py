import logging
import pytest

from settings import test_settings
from testdata.parametrize.person_params import params
from testdata.data.person_data import person_data

data_created = False
person_id = "578593ee-3268-4cd4-b910-8a44cfd05b73"


@pytest.mark.parametrize(
    "query_data, expected_answer", params
)
async def test_persons_search(es_write_data, make_get_request, query_data, expected_answer):
    async def create_persons():
        logging.info("#1 Generating content")

        await es_write_data(person_data, "persons", "id")
        global data_created
        data_created = True
        logging.info("#3 Requesting data from ES via API")

    async def search_persons():
        if not data_created:
            await create_persons()

        response = await make_get_request(test_settings.service_url, "/api/v1/persons/search", query_data)

        logging.info("#4 Checking the answer")

        assert response["status"] == expected_answer["status"]
        assert len(response["body"]) == expected_answer["length"]

    async def persons_id_film():
        
        if not data_created:
            await create_persons()

        response = await make_get_request(test_settings.service_url, f"/api/v1/persons/{person_id}/film", None)

        logging.info("#4 Checking the answer")

        assert response["status"] == expected_answer["status"]
    #    assert len(response["body"]) == expected_answer["length"]


    async def persons_id():
        if not data_created:
            await create_persons()

        response = await make_get_request(test_settings.service_url, f"/api/v1/persons/{person_id}", None)

        logging.info("#4 Checking the answer")

        assert response["status"] == expected_answer["status"]
      #  assert len(response["body"]) == expected_answer["length"]

    async def no_persons_id():

        if not data_created:
            await create_persons()
        person_id = "www-www-www"

        response = await make_get_request(test_settings.service_url, f"/api/v1/persons/{person_id}", None)

        logging.info("#4 Checking the answer")
        assert response["status"] == 404
        assert response["body"]["detail"] == 'Object is not found'
        # assert response["status"] == expected_answer["status"]
        # assert len(response["body"]) == expected_answer["length"]

    await search_persons()
    await persons_id_film()
    await persons_id()
    await no_persons_id()
