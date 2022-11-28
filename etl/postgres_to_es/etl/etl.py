import time
from contextlib import closing
from datetime import datetime

from psycopg2.extras import RealDictCursor

from etl.extractors import FilmworkExtractor
from etl.loaders import FilmworkLoader
from etl.transformers import convert_movies_for_es
from helpers.state import State, RedisStorage
from settings import Settings

from storage_clients.postgres_client import PostgresClient
from storage_clients.redis_client import RedisClient
from storage_clients.elasticsearch_client import ElasticsearchClient


def movie_etl(settings: Settings, state_key: str) -> None:
    with closing(PostgresClient(settings.pg_dsn, cursor_factory=RealDictCursor)) as pg_conn, \
            closing(RedisClient(settings.redis_dsn)) as redis_conn, \
            closing(ElasticsearchClient(settings.es_dsn)) as es_conn:
        pg_conn: PostgresClient
        redis_conn: RedisClient
        es_conn: ElasticsearchClient

        state = State(RedisStorage(redis_conn))

        if not state.exists(state_key):
            state.set_state(state_key, datetime.min.strftime(settings.time_format))

        extractor = FilmworkExtractor(
            pg_conn=pg_conn,
            state=state,
            extract_chunk=settings.load_chunk,
            state_key=state_key,
            time_format=settings.time_format
        )
        loader = FilmworkLoader(
            es_conn=es_conn,
            state=state,
            state_key=state_key
        )

        while True:
            movies = extractor.extract()    # Выгрузка из postgres
            docs = convert_movies_for_es(   # Трансформация в документ индекса
                movies, settings.es_index
            )
            if movies:
                state_value = movies[-1].modified.strftime(
                    settings.time_format        # Дата изменение, которое было записано в ES
                )
                loader.load(docs, state_value)  # Загрузка в ES
            time.sleep(settings.etl_timeout)


