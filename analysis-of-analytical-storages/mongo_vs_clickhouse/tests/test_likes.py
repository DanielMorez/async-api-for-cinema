import logging

from asyncio import run
from typing import Iterable

from data.common import read_csv
from mongo_vs_clickhouse.base import BaseStorage
from mongo_vs_clickhouse.clickhouse.db import ClickHouseStorage
from mongo_vs_clickhouse.mongo.db import MongoStorage

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


click_db = ClickHouseStorage()
mongo_db = MongoStorage()


async def insert_data(clients: list[BaseStorage], file_name: str):
    for client in clients:
        data: Iterable[list[tuple]] = read_csv(
            file_name, client.required_dict_reader, 100_000
        )
        await client.insert("likes", data)
        logger.info(f"Data is successfully inserted into {client}")


async def aggregate_data(clients: list[BaseStorage]):
    for client in clients:
        data = await client.aggregate("likes", "film_id", "stars")
        logger.info(f"Avg data: {data}")


async def main():
    await click_db.init_conn()
    # await click_db.drop_db()
    # await click_db.create_tables()
    #
    # await mongo_db.drop_db()
    #
    # await insert_data([click_db, mongo_db], "../../data/likes.csv")
    await aggregate_data([click_db, mongo_db])

if __name__ == "__main__":
    from mongo_vs_clickhouse.core.stats import STATS

    run(main())
