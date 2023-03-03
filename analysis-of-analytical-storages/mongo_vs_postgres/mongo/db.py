from typing import Iterable

from motor.motor_asyncio import AsyncIOMotorClient

from mongo_vs_postgres.core.decorators import timeit
from mongo_vs_postgres.base_storage import AsyncBaseStorage


class AsyncMongoStorage(AsyncBaseStorage):
    def __init__(
            self,
            dsn: str = "mongodb://root:example@localhost:27017",
            db: str = "ugc_db"
    ):
        self._conn = AsyncIOMotorClient(
            dsn,
            serverSelectionTimeoutMS=5000,
            uuidRepresentation='standard'
        )
        self._db_name = db
        self._db = self._conn[db]

    def __repr__(self):
        return "Mongo"

    @property
    def id_column(self) -> str:
        return "_id"

    @timeit
    async def insert(self, table: str, params: dict) -> None:
        collection = self._db[table]
        await collection.insert_one(params)

    @timeit
    async def find(self, table: str, params: dict) -> list[dict]:
        collection = self._db[table]
        cursor = collection.find(params)
        docs = []
        for doc in await cursor.to_list(length=100):
            docs.append(doc)
        return docs

    @timeit
    async def delete(self, table: str, params: dict) -> None:
        collection = self._db[table]
        await collection.delete_one(params)

    async def drop_db(self) -> None:
        await self._conn.drop_database(self._db_name)
