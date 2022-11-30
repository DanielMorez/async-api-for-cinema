import json
import time
import logging

from contextlib import closing

from etl.etl import movie_etl
from storage_clients.elasticsearch_client import ElasticsearchClient

from settings import Settings

logger = logging.getLogger(__name__)


def main():
    settings = Settings()

    with closing(ElasticsearchClient(settings.es_dsn)) as es_conn:
        if not es_conn.index_exists(settings.es_index):
            with open(f'indexes/{settings.es_index}.json') as file:
                index = json.loads(file.read())
                es_conn.index_create(settings.es_index, index)
            logger.warning(f'Index `{settings.es_index}` created.')

    movie_etl(settings, 'last_modified')


if __name__ == '__main__':
    main()
