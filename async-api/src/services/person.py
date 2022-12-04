import logging

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic.tools import lru_cache

from api.v1.queries_params.persons import PersonListParams
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from services.base_service import BaseService

logger = logging.getLogger(__name__)


class PersonService(BaseService):
    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self._get_person_from_elastic(person_id)
        return person

    async def _get_person_from_elastic(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get(index='persons', id=person_id)
        except NotFoundError:
            logger.debug(f'An error occurred while trying to find person in ES (id: {person_id})')
            return None
        return Person(id=doc['_id'], **doc['_source'])

    async def get_list(self, params: PersonListParams) -> list[Person] | None:
        persons = await self._get_persons_from_elastic(params)
        return persons

    async def _get_persons_from_elastic(self, params: PersonListParams) -> list[Person] | None:
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

            if params.gender:
                body["query"]["bool"]["must"].append(
                    {"query_string": {"query": f"gender:({params.gender})"}}
                )
                use_body = True

            if params.name:
                body["query"]["bool"]["must"].append(
                    {"match": {"name": {"query": params.name, "fuzziness": "AUTO"}}}
                )
                use_body = True

            docs = await self.elastic.search(
                index='persons',
                from_=params.page_size * params.page_number,
                size=params.page_size,
                sort=params.sort,
                body=body if use_body else None
            )
        except NotFoundError:
            logger.debug('An error occurred while trying to get persons in ES)')
            return None
        return [
            Person(id=doc['_id'], **doc['_source']) for doc in docs['hits']['hits']
        ]


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
