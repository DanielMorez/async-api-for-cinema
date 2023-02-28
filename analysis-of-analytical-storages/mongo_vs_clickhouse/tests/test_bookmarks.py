import logging

from typing import Iterable
from random import choice

from data.common import read_csv
from mongo_vs_clickhouse.base import BaseStorage
from mongo_vs_clickhouse.clickhouse.db import ClickHouseStorage
from mongo_vs_clickhouse.core.diagram import show_stats
from mongo_vs_clickhouse.mongo.db import MongoStorage

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


click_db = ClickHouseStorage()
mongo_db = MongoStorage()

get_users = click_db.get_users
get_users_and_films = click_db.get_user_and_films


async def insert_data(clients: list[BaseStorage], file_name: str):
    for client in clients:
        data: Iterable[list[tuple]] = read_csv(
            file_name, client.required_dict_reader, 100_000
        )
        await client.insert("bookmarks", data)
        logger.info(f"Data is successfully inserted into {client}")


async def search_query(clients: list[BaseStorage], queries_amount: int = 10):
    for client in clients:
        for _ in range(queries_amount):
            users = await get_users("bookmarks")
            params = {"user_id": str(choice(users)[0])}
            bookmarks = await client.find("bookmarks", params)
            logger.info(f"User `{params['user_id']}` has {len(bookmarks)} of bookmarks")


async def delete_query(clients: list[BaseStorage], queries_amount: int = 10):
    for client in clients:
        for _ in range(queries_amount):
            user_id, film_id = choice(await get_users_and_films("bookmarks"))
            params = {"user_id": user_id, "film_id": film_id}
            await client.delete("bookmarks", params)
            logger.info(f"Bookmark of user `{params['user_id']}` is deleted")


async def main():
    await click_db.init_conn()
    await click_db.drop_db()
    await click_db.create_tables()

    await mongo_db.drop_db()

    await insert_data([click_db, mongo_db], "../../data/bookmarks_.csv")
    await search_query([click_db, mongo_db])
    await delete_query([click_db, mongo_db])


if __name__ == "__main__":
    import asyncio

    from mongo_vs_clickhouse.core.stats import STATS

    asyncio.run(main(), debug=True)

    show_stats(STATS)
    input()
