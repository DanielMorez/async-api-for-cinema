import asyncio
from contextlib import closing
from datetime import datetime

from psycopg2.extras import RealDictCursor

from etl.extractors import EXTRACTORS
from etl.loaders import ESLoader
from etl.queries import QUERIES
from etl.transformers import TRANSFORMERS
from helpers.state import State, RedisStorage
from models.movie import Movie
from models.person import Person
from models.genre import Genre
from settings import Settings

from storage_clients.postgres_client import PostgresClient
from storage_clients.redis_client import RedisClient
from storage_clients.elasticsearch_client import ElasticsearchClient


async def etl(settings: Settings, index: str) -> None:
    with closing(PostgresClient(settings.pg_dsn, cursor_factory=RealDictCursor)) as pg_conn, \
            closing(RedisClient(settings.redis_dsn)) as redis_conn, \
            closing(ElasticsearchClient(settings.es_dsn)) as es_conn:
        pg_conn: PostgresClient
        redis_conn: RedisClient
        es_conn: ElasticsearchClient

        state = State(RedisStorage(redis_conn))
        state_key = f'{index}_last_modified'
        if not state.exists(state_key):
            state.set_state(state_key, datetime.min.strftime(settings.time_format))

        extractor_class = EXTRACTORS[index]

        extractor = extractor_class(
            pg_conn=pg_conn,
            state=state,
            query=QUERIES[index],
            state_key=state_key,
            extract_chunk=settings.load_chunk
        )
        loader = ESLoader(
            es_conn=es_conn,
            state=state,
            state_key=state_key
        )
        convert = TRANSFORMERS[index]

        while True:
            data: list[Movie | Person | Genre] = extractor.extract()  # Выгрузка из postgres
            if data:
                docs = convert(data, index)     # Трансформация в документ индекса
                state_value = data[-1].modified.strftime(
                    settings.time_format        # Дата изменение, которое было записано в ES
                )
                loader.load(docs, state_value)  # Загрузка в ES
            await asyncio.sleep(settings.etl_timeout)


