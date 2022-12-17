import logging
from http import HTTPStatus

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, HTTPException
from pydantic.tools import lru_cache

from api.v1.queries_params.persons import PersonSearchParams
from db.cache_base import AsyncCacheStorage
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from models.person import Person
from services.base_service import BaseService

logger = logging.getLogger(__name__)


class PersonService(BaseService):
    index = "persons"

    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self._get_person_from_elastic(person_id)
        return person

    async def _get_person_from_elastic(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get(index=self.index, id=person_id)
        except NotFoundError:
            logger.debug(
                f"An error occurred while trying to find person in ES (id: {person_id})"
            )
            return None
        return Person(id=doc["_id"], **doc["_source"])

    async def get_list(self, params: PersonSearchParams) -> list[Person] | None:
        persons = await self._get_persons_from_elastic(params)
        return persons

    async def _get_persons_from_elastic(
        self, params: PersonSearchParams
    ) -> list[Person] | None:
        try:
            body = None
            if params.query:
                body = {"query": {"query_string": {"query": params.query}}}
            docs = await self.elastic.search(
                index=self.index,
                from_=params.page_size * params.page_number,
                size=params.page_size,
                body=body,
            )
        except NotFoundError:
            logger.debug("An error occurred while trying to get persons in ES)")
            return None
        return [Person(id=doc["_id"], **doc["_source"]) for doc in docs["hits"]["hits"]]

    async def get_person_films(self, person_id: str) -> list[Film]:
        person: Person = await self.get_by_id(person_id)
        if not person:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="person not found"
            )
        films_ids = [film.id for film in person.films]
        films: list[Film] = await self._get_person_films_from_es(films_ids)
        return films

    async def _get_person_films_from_es(self, film_ids: list[str]) -> list[Film]:
        try:
            body = {"query": {"ids": {"values": film_ids}}}
            docs = await self.elastic.search(
                index="movies",
                body=body,
            )
        except NotFoundError:
            logger.debug("An error occurred while trying to get films in ES)")
            return None
        return [Film(id=doc["_id"], **doc["_source"]) for doc in docs["hits"]["hits"]]


@lru_cache()
def get_person_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache, elastic)
