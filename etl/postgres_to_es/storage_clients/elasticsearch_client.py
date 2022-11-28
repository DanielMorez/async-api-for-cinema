import logging

import elastic_transport
from elasticsearch import Elasticsearch, helpers
from pydantic import AnyHttpUrl

from helpers.backoff import backoff, reconnect as storage_reconnect
from helpers.exceptions import ElasticsearchNotConnectedError
from storage_clients.base_client import BaseClient


logger = logging.getLogger(__name__)


class ElasticsearchClient(BaseClient):
    """Layer over Elasticsearch for backoff implementation and closing connections."""
    base_exceptions = elastic_transport.ConnectionError
    _connection: Elasticsearch

    def __init__(self, dsn: AnyHttpUrl, *args, **kwargs):
        super().__init__(dsn, *args, **kwargs)

    @property
    def is_connected(self) -> bool:
        return self._connection and self._connection.ping()

    @backoff()
    def connect(self) -> None:
        self._connection = Elasticsearch(self.dsn, *self.args, **self.kwargs)
        if not self.is_connected:
            raise ElasticsearchNotConnectedError(
                f'Connection is not properly established for: `{self.__repr__()}`'
            )
        logger.info(f'Established new connection for: {self}')

    def reconnect(self) -> None:
        super().reconnect()

    @backoff()
    def close(self) -> None:
        super().close()

    @backoff()
    @storage_reconnect
    def index_exists(self, index: str) -> None:
        return self._connection.indices.exists(index=index)

    @backoff()
    @storage_reconnect
    def index_create(self, index: str, body: dict) -> None:
        return self._connection.indices.create(index=index, body=body)

    @backoff()
    @storage_reconnect
    def bulk(self, *args, **kwargs) -> None:
        helpers.bulk(self._connection, *args, **kwargs)


if __name__ == '__main__':
    import json
    from contextlib import closing

    url = 'http://127.0.0.1:9200/'
    with closing(ElasticsearchClient(url)) as es:
        if not es.index_exists('movies'):
            with open('../indexes/movies.json') as file:
                index = json.loads(file.read())
            es.index_create('movies', index)

        es.bulk(
            [
                {
                    "_index": "movies",
                    "_id": '1',
                    "_source": {
                        "title": 'test',
                        "genres": [{'id': 1, 'name': 'test'}],
                        "genres_names": ['test'],
                        "imdb_rating": 9.1,
                        "description": 'test',
                        "actors": [],
                        "actors_names": [],
                        "writers": [],
                        "writers_names": [],
                        "directors": [],
                        "directors_names": [],
                    }
                }
            ]
        )
