import logging

from random import choice
from data.common import read_csv
from mongo_vs_postgres.config import settings
from mongo_vs_postgres.base_storage import AsyncBaseStorage
from mongo_vs_postgres.core.diagram import show_stats
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
        "insert": {},
        "find": {},
        "delete": {},
    },
    "Mongo": {
        "insert": {},
        "find": {},
        "delete": {},
    },
}
users: list[str] = list()  # Collection of user ids
bookmarks_ids: list[str] = list()


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
                if row["_id"] not in bookmarks_ids:
                    bookmarks_ids.append(row["_id"])
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
                    logger.info(f"{counter} insert requests to {client} - time (in seconds) {avg}")


async def test_find(clients: list[AsyncBaseStorage], amount: int = 10_000):
    logger.info("=== START OF LOOKING FOR BOOKMARKS ===")
    for client in clients:
        counter = 0
        for _ in range(amount):
            params = {"user_id": choice(users)}
            bookmarks = await client.find("bookmarks", params)
            counter += 1
            if counter in CHECKPOINTS:
                avg = get_avg(STATS[str(client)]["bookmarks_find"])
                current_stats[str(client)]["find"][counter] = avg
                STATS[str(client)]["bookmarks_find"] = []
                logger.info(f"{counter} find requests to {client} - time (in seconds) {avg}")


async def test_delete(clients: list[AsyncBaseStorage], amount: int = 10_000):
    logger.info("=== START OF DELETING BOOKMARKS ===")
    for client in clients:
        counter = 0
        for _ in range(amount):
            params = {client.id_column: choice(bookmarks_ids)}
            bookmarks_ids.pop(bookmarks_ids.index(params[client.id_column]))
            await client.delete("bookmarks", params)
            counter += 1
            if counter in CHECKPOINTS:
                avg = get_avg(STATS[str(client)]["bookmarks_delete"])
                current_stats[str(client)]["delete"][counter] = avg
                STATS[str(client)]["bookmarks_delete"] = []
                logger.info(f"{counter} delete requests to {client} - time (in seconds) {avg}")


async def main():
    await pg_storage.init_connection()
    await pg_storage.drop_db()
    await mongo_storage.drop_db()
    await pg_storage.create_tables()

    clients = [pg_storage, mongo_storage]

    await test_insert(clients, "../../data/bookmarks.csv")
    await test_find(clients)
    await test_delete(clients)
    logger.info(current_stats)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
