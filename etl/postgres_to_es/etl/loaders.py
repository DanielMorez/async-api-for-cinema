import logging

from helpers.state import State
from storage_clients.elasticsearch_client import ElasticsearchClient

logger = logging.getLogger(__name__)


class ESLoader:
    def __init__(
            self,
            es_conn: ElasticsearchClient,
            state: State,
            state_key: str,
    ):
        self.es_conn = es_conn
        self.state = state
        self.state_key = state_key

    def load(self, docs, state_value: object):
        self.es_conn.bulk(docs)
        self.state.set_state(
            self.state_key, state_value
        )
        logger.info(f'Completed upload to Elasticsearch.')
