import os
import json
import asyncio
import logging

from contextlib import closing

from etl.etl import etl
from storage_clients.elasticsearch_client import ElasticsearchClient

from settings import Settings

logger = logging.getLogger(__name__)


async def main():
    settings = Settings()

    with closing(ElasticsearchClient(settings.es_dsn)) as es_conn:
        for es_index in settings.es_indexes:
            if not es_conn.index_exists(es_index):
                if os.path.exists(f'indexes/{es_index}.json'):
                    with open(f'indexes/{es_index}.json') as file:
                        index = json.loads(file.read())
                        es_conn.index_create(es_index, index)
                    logger.warning(f'Index `{es_index}` created.')
                else:
                    logger.warning(f'Index `{es_index}` does not exist.')
                    raise Exception(
                        f'Index `{es_index}` does not exist. '
                        f'Add `{es_index}`.json with settings of index in dir: indexes/'
                    )

    logger.warning(f'Start ETL process for indexes {settings.es_indexes}.')
    await asyncio.gather(
        *(etl(settings, index) for index in settings.es_indexes)
    )


if __name__ == '__main__':
    asyncio.run(main())
