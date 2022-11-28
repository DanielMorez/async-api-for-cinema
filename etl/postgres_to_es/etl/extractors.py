import logging

from helpers.state import State
from models import Movie
from storage_clients.postgres_client import PostgresClient
from etl.queries.movies import QUERY_TO_GET_LAST_MODIFIED

logger = logging.getLogger(__name__)


class FilmworkExtractor:
    def __init__(
        self,
        pg_conn: PostgresClient,
        state: State,
        extract_chunk: int,
        state_key: str,
        time_format: str,
    ):
        self.state = state
        self.pg_conn = pg_conn
        self.extract_chunk = extract_chunk
        self.state_key = state_key
        self.time_format = time_format

    def extract(self) -> list[Movie]:
        movies: list[Movie] = []

        last_modified = self.state.get_state(
            self.state_key
        )

        with self.pg_conn.cursor() as cursor:
            cursor.execute(
                QUERY_TO_GET_LAST_MODIFIED.format(
                    last_modified=last_modified,
                    extract_chunk=self.extract_chunk
                )
            )
            while results := cursor.fetchmany(self.extract_chunk):
                movies = [Movie(**data) for data in results]

        logger.info(f'Finished extracting movies. Collected {len(movies)} units.')
        return movies
