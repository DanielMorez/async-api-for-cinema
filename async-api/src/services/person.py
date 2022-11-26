from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id возвращает объект персоны. Он опционален, так как персона может отсутствовать в базе
    async def get_by_id(self, person_id: str) -> Optional[Person]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        person = await self._person_from_cache(person_id)
        if not person:
            # Если персоны нет в кеше, то ищем его в Elasticsearch
            person = await self._get_person_from_elastic(person_id)
            if not person:
                # Если он отсутствует в Elasticsearch, значит, персоны вообще нет в базе
                return None
            # Сохраняем персону  в кеш
            await self._put_person_to_cache(person)

        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get(index='persons', id=person_id)
        except NotFoundError:
            return None
        return Person(
            id=person_id,
            **doc.body['_source']
        )

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        # Пытаемся получить данные о персоне из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(person_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: Person):
        # Сохраняем данные о персоне, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(person.id, person.json(), expire=PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
