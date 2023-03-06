from motor.motor_asyncio import AsyncIOMotorClient

mongo: AsyncIOMotorClient = None


async def get_mongo() -> AsyncIOMotorClient:
    return mongo
