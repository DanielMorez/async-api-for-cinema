from typing import Any

from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from api.v1.queries_params.base import QueryListBaseModel


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    def get_by_id(self, id: str) -> Any | None:
        raise NotImplementedError

    def get_list(self, params: QueryListBaseModel) -> list | None:
        raise NotImplementedError
