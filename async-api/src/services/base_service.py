from typing import Any

from elasticsearch import AsyncElasticsearch

from api.v1.queries_params.base import QueryListBaseModel
from db.cache_base import AsyncCacheStorage


class BaseService:
    def __init__(self, cache: AsyncCacheStorage, elastic: AsyncElasticsearch):
        self.cache = cache
        self.elastic = elastic

    def get_by_id(self, id: str) -> Any | None:
        raise NotImplementedError

    def get_list(self, params: QueryListBaseModel) -> list | None:
        raise NotImplementedError
