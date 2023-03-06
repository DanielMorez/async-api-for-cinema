from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_mongo
from services.base_service import BaseService
from services.mongo import MongoService

service: BaseService = None


async def get_service(
    client: AsyncIOMotorClient = Depends(get_mongo)
) -> BaseService:
    return MongoService(client)
