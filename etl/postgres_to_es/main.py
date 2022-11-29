import os
import json
import asyncio
import logging

from contextlib import closing

from etl.etl import etl
from storage_clients.elasticsearch_client import ElasticsearchClient

from settings import Settings

logger = logging.getLogger(__name__)


def main():
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

    for index in settings.es_indexes:
        logger.warning(f'Start ETL process for index `{es_index}`.')
        asyncio.run(etl(settings, index))


if __name__ == '__main__':
    main()
