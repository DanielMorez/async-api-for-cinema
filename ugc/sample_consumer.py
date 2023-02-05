import asyncio
from contextlib import asynccontextmanager

from adapters.broker import KafkaConsumerClient
from core.config import settings


@asynccontextmanager
async def kafka_consumer(take_oldest=False):
    client = KafkaConsumerClient(
        f"{settings.broker.host}:{settings.broker.port}",
        f"{settings.broker.topic}",
        take_oldest=take_oldest,
    )
    await client.startup()
    yield client
    await client.shutdown()


async def main(loop=None):
    async with kafka_consumer(take_oldest=True) as consumer:
        async for msg in consumer.receive():
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main(loop=loop))
