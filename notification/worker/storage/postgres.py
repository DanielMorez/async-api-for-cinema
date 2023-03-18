import contextlib
import time
import psycopg2

from typing import Any
from psycopg2.extensions import connection as pg_conn, cursor as pg_cursor
from psycopg2.sql import SQL
from pydantic import PostgresDsn

from helpers.backoff import backoff, reconnect as storage_reconnect
from storage.base import BaseClient, ClientInterface
from logging import getLogger


logger = getLogger(__name__)


class PostgresClient(BaseClient):
    _connection: pg_conn

    def __init__(self, dsn: PostgresDsn, *args, **kwargs):
        super().__init__(dsn, *args, **kwargs)
        self._connection.autocommit = True

    @backoff()
    def connect(self) -> None:
        self._connection = psycopg2.connect(dsn=self.dsn, *self.args, **self.kwargs)
        logger.info(f'Established new connection for: {self}')

    @property
    def is_connected(self) -> bool:
        return self._connection and not self._connection.closed

    @backoff()
    @contextlib.contextmanager
    def cursor(self) -> 'PostgresCursor':
        cursor: PostgresCursor = PostgresCursor(self)

        yield cursor

        cursor.close()

    def reconnect(self) -> None:
        if not self.is_connected:
            logger.info(f'Trying to reconnect to: {self}.')
            self.connect()

    @backoff()
    def close(self) -> None:
        if self.is_connected:
            self._connection.close()
            logger.info(f'Closed connection for: {self}.')

        self._connection = None


class PostgresCursor(ClientInterface):
    base_exceptions = psycopg2.OperationalError
    _cursor: pg_cursor

    def __init__(self, connection: PostgresClient, *args, **kwargs):
        self._connection = connection
        self.connect(*args, **kwargs)

    def __repr__(self):
        return f'Postgres cursor with connection dsn: {self._connection.dsn}'

    @property
    def is_cursor_opened(self) -> bool:
        return self._cursor and not self._cursor.closed

    @property
    def is_connection_opened(self) -> bool:
        return self._connection.is_connected

    @property
    def is_connected(self) -> bool:
        return self.is_connection_opened and self.is_cursor_opened

    @backoff()
    def connect(self, *args, **kwargs) -> None:
        # noinspection PyProtectedMember
        self._cursor: pg_cursor = self._connection._connection.cursor(*args, **kwargs)
        logger.debug(f'Created new cursor for: {self}.')

    def reconnect(self) -> None:
        if not self.is_connection_opened:
            logger.debug(f'Trying to reconnect to: {self}.')
            self._connection.connect()

        if not self.is_cursor_opened:
            logger.debug(f'Trying to create new cursor for: {self}.')
            self.connect()

    @backoff()
    def close(self) -> None:
        if self.is_cursor_opened:
            self._cursor.close()
            logger.debug(f'Cursor closed for: {self}.')

    @backoff()
    @storage_reconnect
    def execute(self, query: str | SQL, *args, **kwargs) -> None:
        self._cursor.execute(query, *args, **kwargs)

    @backoff()
    @storage_reconnect
    def fetchmany(self, chunk: int) -> list[Any]:
        return self._cursor.fetchmany(size=chunk)


if __name__ == '__main__':
    from contextlib import closing

    url = 'postgresql://app:123qwe@127.0.0.1:5432/movies_database'
    with closing(PostgresClient(url)) as conn:
        with conn.cursor() as cursor:
            while True:
                a = cursor.execute(
                    '''SELECT COUNT(*) FROM notification.tasks;'''
                )
                print(cursor.fetchmany(100))
                time.sleep(5)
