import logging

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


def get_avg(data: list[float]) -> float:
    if not data:
        return 0
    return sum(data) / len(data)


async def test_insert(
    clients: list[AsyncBaseStorage],
    file_csv: str
):
    for client in clients:
        generator = read_csv(file_csv, dict_reader=True)
        counter = 0
        for rows in generator:
            for row in rows:
                if isinstance(client, AsyncPostgresStorage):
                    row["id"] = row["_id"]
                    del row["_id"]
                await client.insert("bookmarks", row)
                counter += 1
                if counter in CHECKPOINTS:
                    current_stats[str(client)]["insert"][counter] = get_avg(STATS[str(client)]["bookmarks_insert"])
                    STATS[str(client)]["bookmarks_insert"] = []


async def main():
    await pg_storage.init_connection()
    await pg_storage.drop_db()
    await pg_storage.create_tables()

    clients = [pg_storage, mongo_storage]

    await test_insert(clients, "../../data/bookmarks_.csv")

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
