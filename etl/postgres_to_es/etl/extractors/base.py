import logging

from helpers.state import State
from storage_clients.postgres_client import PostgresClient

logger = logging.getLogger(__name__)


class BaseExtractor:
    def __init__(
            self,
            pg_conn: PostgresClient,
            state: State,
            query: str,
            state_key: str,
            extract_chunk: int
    ):
        self.pg_conn = pg_conn
        self.state = state
        self.query = query
        self.state_key = state_key
        self.extract_chunk = extract_chunk

    def get_content(self) -> list[dict] | None:
        with self.pg_conn.cursor() as cursor:
            cursor.execute(
                self.query.format(
                    last_modified=self.last_modified,
                    extract_chunk=self.extract_chunk
                )
            )
            while results := cursor.fetchmany(self.extract_chunk):
                yield results

    @property
    def last_modified(self):
        """ Get last modified content """
        return self.state.get_state(self.state_key)

    def extract(self) -> None:
        raise NotImplementedError
