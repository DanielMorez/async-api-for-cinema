import logging

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic.tools import lru_cache

from api.v1.queries_params.genres import GenreListParams
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.base_service import BaseService

logger = logging.getLogger(__name__)


class GenreService(BaseService):
    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre = await self._get_genre_from_elastic(genre_id)
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.elastic.get(index='genres', id=genre_id)
        except NotFoundError:
            logger.debug(f'An error occurred while trying to find genre in ES (id: {genre_id})')
            return None
        return Genre(id=doc['_id'], **doc['_source'])

    async def get_list(self, params: GenreListParams) -> list[Genre] | None:
        persons = await self._get_genres_from_elastic(params)
        return persons

    async def _get_genres_from_elastic(self, params: GenreListParams) -> list[Genre] | None:
        try:
            body = {"query": {"bool": {"must": []}}}
            use_body = False

            if params.name:
                body["query"]["bool"]["must"].append(
                    {"query_string": {"query": f"name:({params.name})"}}
                )
                use_body = True

            docs = await self.elastic.search(
                index='genres',
                from_=params.page_size * params.page_number,
                size=params.page_size,
                sort=params.sort,
                body=body if use_body else None
            )
        except NotFoundError:
            logger.debug('An error occurred while trying to get genres in ES)')
            return None
        return [
            Genre(id=doc['_id'], **doc['_source']) for doc in docs['hits']['hits']
        ]


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
