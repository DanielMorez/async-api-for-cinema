import uuid
import json
import datetime
import logging
import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from settings import test_settings


logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_search():
    logger.debug("#1 Generating content")

    es_data = [{
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

    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': test_settings.es_index, '_id': str(uuid.uuid4())}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    logger.debug("#2 Load content to ES")

    es_client = AsyncElasticsearch(hosts=[test_settings.es_dsn])
    response = await es_client.bulk(operations=str_query, refresh=True)
    await es_client.close()
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')

    logger.debug("#3 Requesting data from ES via API")

    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/films/search'
    query_data = {'query': 'The Star'}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    logger.debug("#4 Checking the answer")

    assert status == 200
    assert len(body) == 50
