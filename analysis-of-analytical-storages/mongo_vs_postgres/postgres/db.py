import asyncpg
from pydantic import PostgresDsn

from mongo_vs_postgres.postgres import queries
from mongo_vs_postgres.core.decorators import timeit
from mongo_vs_postgres.base_storage import AsyncBaseStorage


class AsyncPostgresStorage(AsyncBaseStorage):
    _conn = None

    def __init__(self, dsn: PostgresDsn):
        self._dsn = dsn

    def __repr__(self):
        return "Postgres"

    async def init_connection(self):
        self._conn = await asyncpg.connect(self._dsn)

    @timeit
    async def insert(self, table: str, params: dict) -> None:
        if not params:
            return
        columns = "(" + ",".join(params.keys()) + ")"
        values = convert_to_pg_values(params)
        await self._conn.execute(
            queries.INSERT.format(
                table=table,
                columns=columns
            ) + values
        )

    @timeit
    async def find(self, table: str, params: dict) -> list[dict]:
        query = queries.SELECT_WHERE + convert_to_pg_condition(params)
        data = await self._conn.fetch(query)
        return data

    @timeit
    async def delete(self, table: str, params: dict) -> None:
        query = queries.DELETE_WHERE + convert_to_pg_condition(params)
        await self._conn.execute(query)

    async def drop_db(self) -> None:
        await self._conn.execute(queries.DROP_ALL_TABLES)

    async def create_tables(self) -> None:
        for query in queries.CREATE_TABLES:
            await self._conn.execute(query)


def convert_to_pg(value: str | int) -> str:
    if isinstance(value, str):
        return f"'{value}'"
    if value.isdigit():
        return str(value)


def convert_to_pg_values(params: dict) -> str:
    data = [convert_to_pg(v) for v in params.values()]
    return "(" + ",".join(data) + ")"


def convert_to_pg_condition(params: dict) -> str:
    return " AND ".join(
        [f"{k} = {convert_to_pg(v)}" for k, v in params.items()]
    )
