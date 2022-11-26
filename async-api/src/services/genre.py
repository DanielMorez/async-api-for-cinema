from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id возвращает объект жанра. Он опционален, так как жанр может отсутствовать в базе
    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            # Если жанра нет в кеше, то ищем его в Elasticsearch
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                # Если он отсутствует в Elasticsearch, значит, жанра вообще нет в базе
                return None
            # Сохраняем жанр  в кеш
            await self._put_genre_to_cache(genre)

        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get(index='genres', id=genre_id)
        except NotFoundError:
            return None
        return Genre(
            id=genre_id,
            **doc.body['_source']
        )

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        # Пытаемся получить данные о жанре из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(genre_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        # Сохраняем данные о жанре, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(genre.id, genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
