import json
from functools import lru_cache
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from loguru import logger

from services.utils import get_key_by_args
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def all(self, **kwargs) -> list[Optional[Film]]:
        films = await self._films_from_cache(**kwargs)
        if not films:
            films = await self._get_films_from_elastic(**kwargs)
            if not films:
                return []
            await self._put_films_to_cache(films, **kwargs)
        return films

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    @staticmethod
    async def _make_film_from_es_doc(doc: dict) -> Film:
        genre = doc['_source'].get('genre')
        if genre and isinstance(genre, str):
            doc['_source']['genre'] = [{'id': item, 'name': item} for item in genre.split(' ')]
        film = Film(id=doc['_id'], **doc['_source'])
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

    async def _get_films_from_elastic(self, **kwargs) -> Optional[list[Film]]:
        page_size = kwargs.get('page_size', 10)
        page = kwargs.get('page', 1)
        sort = kwargs.get('sort', '')
        genre = kwargs.get('genre', None)
        query = kwargs.get('query', None)
        body = None
        if genre:
            body = {
                'query': {
                    'query_string': {
                        'default_field': 'genre',
                        'query': genre
                    }
                }
            }
        if query:
            body = {
                'query': {
                    'match': {
                        'title': {
                            'query': query,
                            'fuzziness': 1,
                            'operator': 'and'
                        }
                    }
                }
            }
        try:
            docs = await self.elastic.search(index='movies', body=body,
                                             params={'size': page_size, 'from': page - 1, 'sort': sort,})
        except NotFoundError:
            logger.debug('An error occurred while trying to get films in ES)')
            return None
        return [await FilmService._make_film_from_es_doc(doc) for doc in docs['hits']['hits']]

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            logger.debug(f'The film was not found in the cache (id: {film_id})')
            return None
        film = Film.parse_raw(data)
        return film

    async def _films_from_cache(self, **kwargs) -> Optional[list[Film]]:
        key = await get_key_by_args(**kwargs)
        data = await self.redis.get(key)
        if not data:
            logger.debug('Films was not found in the cache')
            return None
        return [Film.parse_raw(item) for item in orjson.loads(data)]

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_films_to_cache(self, films: list[Film], **search_params):
        key = await get_key_by_args(**search_params)
        await self.redis.set(key,
                             orjson.dumps([film.json() for film in films]),
                             ex=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
