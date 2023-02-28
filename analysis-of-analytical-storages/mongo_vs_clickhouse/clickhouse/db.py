from aiocache import cached
from typing import Iterable

# from clickhouse_driver import Client
from asynch import connect

from mongo_vs_clickhouse.core.decorators import timeit
from mongo_vs_clickhouse.base import BaseStorage
from mongo_vs_clickhouse.clickhouse.queries import (
    BOOKMARKS, DROP_DB, CREATE_DB,
    INSERT_QUERIES, FIND_QUERIES, DELETE_QUERIES,
    SELECT_USERS, SELECT_FILMS, LIKES, AGGREGATE
)


class ClickHouseStorage(BaseStorage):
    required_dict_reader = False

    def __init__(self, host: str = "localhost", port: int = 9000):
        self._conn = connect(host=host, port=port)

    async def init_conn(self):
        self._conn = await self._conn

    def __repr__(self):
        return "ClickHouse"

    @property
    def create_tables_queries(self) -> list[str]:
        return [CREATE_DB, BOOKMARKS, LIKES]

    @property
    def drop_db_query(self) -> str:
        return DROP_DB

    async def _execute(self, query: str, data: list[tuple | dict] = None) -> list[tuple] | None:
        async with self._conn.cursor() as cursor:
            await cursor.execute(query, data)
            data = await cursor.fetchall()
        return data

    async def create_tables(self) -> None:
        for query in self.create_tables_queries:
            await self._execute(query)

    async def drop_db(self) -> None:
        await self._execute(self.drop_db_query)

    @timeit
    async def insert(self, table: str, data_generator: Iterable[list[tuple]]) -> None:
        for data in data_generator:
            await self._execute(INSERT_QUERIES[table], data)

    @timeit
    async def find(self, table: str, params: list[dict]) -> list[tuple]:
        return await self._execute(FIND_QUERIES[table], params)

    @timeit
    async def delete(self, table: str, params: list[dict]) -> None:
        await self._execute(DELETE_QUERIES[table], params)

    @timeit
    async def aggregate(
        self, table: str, group_field: str, aggregate_field: str, limit: int = 10
    ) -> list[tuple]:
        return await self._execute(
            AGGREGATE.format(table=table, group_field=group_field, aggregate_field=aggregate_field, limit=limit)
        )

    async def query(self, query: str, params: list[dict] = None) -> list[tuple]:
        return await self._execute(query, params)

    @cached()
    async def get_users(self, table: str) -> list[tuple[str]]:
        return await self._execute(SELECT_USERS.format(table=table))

    @cached()
    async def get_user_and_films(self, table: str) -> list[tuple[str, str]]:
        return await self._execute(SELECT_FILMS.format(table=table))
