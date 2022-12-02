import logging
from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from api.v1.queries_params.films import FilmListParams
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

logger = logging.getLogger(__name__)

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_list(self, params: FilmListParams) -> list[Optional[Film]]:
        films = await self._get_films_from_elastic(params)
        return films

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._get_film_from_elastic(film_id)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            logger.debug(f'An error occurred while trying to find film in ES (id: {film_id})')
            return None
        genre = doc['_source'].get('genre')
        if genre and isinstance(genre, str):
            doc['_source']['genre'] = [{'id': item, 'name': item} for item in genre.split(' ')]
        return Film(id=doc['_id'], **doc['_source'])

    async def _get_films_from_elastic(self, params: FilmListParams) -> Optional[list[Film]]:
        try:
            body = {"query": {"bool": {"must": []}}}
            use_body = False

            for param_name in params.string_query_params:
                param_value = getattr(params, param_name)
                if param_value:
                    body["query"]["bool"]["must"].append(
                        {"query_string": {"query": f"{param_name}_names:({param_value})"}}
                    )
                    use_body = True

            if params.contains_rating_filter:
                body["query"]["bool"]["must"].append({
                    "range": {
                        "imdb_rating": {
                            "gte": params.imdb_rating_gt, "lte": params.imdb_rating_lt
                        }
                    }
                })

            docs = await self.elastic.search(
                index='movies',
                from_=params.page_size * params.page_number,
                size=params.page_size,
                sort=params.sort,
                body=body if use_body else None
            )
        except NotFoundError:
            logger.debug('An error occurred while trying to get films in ES)')
            return None
        return [
            Film(id=doc['_id'], **doc['_source']) for doc in docs['hits']['hits']
        ]


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
