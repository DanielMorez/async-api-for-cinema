import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from random import randint

from adapters.broker import KafkaProducerClient
from core.config import settings


@asynccontextmanager
async def kafka_producer():
    print(f"{settings.broker.host}:{settings.broker.port}")
    client = KafkaProducerClient(
        f"{settings.broker.host}:{settings.broker.port}"
    )
    await client.startup()
    yield client
    await client.shutdown()


async def main(loop=None):
    async with kafka_producer() as producer:
        user_id = str(f"u{randint(1, 10)}")
        movie_id = str(f"m{randint(1, 10)}")
        start = datetime.now()
        finish = start + timedelta(seconds=randint(10, 100))

        dt_format = "%Y-%m-%d %H:%M:%S"

        message = {
            "user_id": user_id,
            "movie_id": movie_id,
            "start": start.strftime(dt_format),
            "finish": finish.strftime(dt_format),
        }
        key = f"{user_id}:{movie_id}"
        # print(message, key)
        await producer.send(settings.broker.topic, message, key)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main(loop=loop))
