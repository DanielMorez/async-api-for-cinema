import logging

from random import choice
from data.common import read_csv
from mongo_vs_postgres.config import settings
from mongo_vs_postgres.base_storage import AsyncBaseStorage
from mongo_vs_postgres.core.stats import CHECKPOINTS, STATS
from mongo_vs_postgres.mongo.db import AsyncMongoStorage
from mongo_vs_postgres.postgres.db import AsyncPostgresStorage

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


pg_storage = AsyncPostgresStorage(settings.PG_DSN)
mongo_storage = AsyncMongoStorage(settings.MONGO_DSN, settings.MONGO_DB)

current_stats = {
    "Postgres": {
        "insert": {}
    },
    "Mongo": {
        "insert": {}
    },
}
users: list[str] = list()  # Collection of user ids


def get_avg(data: list[float]) -> float:
    if not data:
        return 0
    return sum(data) / len(data)


async def test_insert(
    clients: list[AsyncBaseStorage],
    file_csv: str
):
    logger.info("=== START OF DATA INSERTING ===")
    for client in clients:
        generator = read_csv(file_csv, dict_reader=True)
        counter = 0
        for rows in generator:
            for row in rows:
                if isinstance(client, AsyncPostgresStorage):
                    row["id"] = row["_id"]
                    del row["_id"]
                    if row["user_id"] not in users:
                        users.append(row["user_id"])
                await client.insert("bookmarks", row)
                counter += 1
                if counter in CHECKPOINTS:
                    avg = get_avg(STATS[str(client)]["bookmarks_insert"])
                    current_stats[str(client)]["insert"][counter] = avg
                    STATS[str(client)]["bookmarks_insert"] = []
                    logger.info(f"{counter} requests to {client} - time (in seconds) {avg}")


async def test_find(clients: list[AsyncBaseStorage], amount: int = 100_000):
    logger.info("=== START OF LOOKING FOR BOOKMARKS ===")
    for client in clients:
        for _ in range(amount):
            params = {"user_id": choice(users)}
            bookmarks = await client.find("bookmarks", )
            logger.info(f"User `{params['user_id']}` has {len(bookmarks)} of bookmarks")


async def test_delete(clients: list[AsyncBaseStorage], amount: int = 50_000):
    logger.info("=== START OF DELETING BOOKMARKS ===")
    for client in clients:
        for _ in range(amount):
            params = {"user_id": choice(users)}
            await client.delete("bookmarks", params)
            logger.info(f"Bookmarks of user `{params['user_id']} are deleted`")


async def main():
    await pg_storage.init_connection()
    await pg_storage.drop_db()
    await mongo_storage.drop_db()
    await pg_storage.create_tables()

    clients = [pg_storage, mongo_storage]

    await test_insert(clients, "../../data/bookmarks.csv")
    await test_find(clients)
    await test_delete(clients)
    a = 1

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
