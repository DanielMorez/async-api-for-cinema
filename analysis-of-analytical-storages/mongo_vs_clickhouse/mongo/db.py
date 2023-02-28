from typing import Iterable

# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

from mongo_vs_clickhouse.core.decorators import timeit
from mongo_vs_clickhouse.base import BaseStorage


class MongoStorage(BaseStorage):
    required_dict_reader = True

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

    @timeit
    async def insert(self, table: str, data_generator: Iterable[list[dict]]) -> None:
        collection = self._db[table]
        for docs in data_generator:
            await collection.insert_many(docs)

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

    @timeit
    async def aggregate(
        self, table: str, group_field: str, aggregate_field: str, limit: int = 10
    ) -> list[tuple]:
        collection = self._db[table]
        cursor = collection.aggregate([
            {"$group": {group_field: f"${group_field}", "avg_val": {"$avg": f"${aggregate_field}"}}},
            {"$sort": {aggregate_field: -1}},
            {"$limit": limit}
        ])
        docs = []
        for doc in await cursor.to_list(length=100):
            docs.append(doc)
        return docs

    async def drop_db(self) -> None:
        await self._conn.drop_database(self._db_name)
