from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache import JsonCoder
from fastapi_cache.decorator import cache
from fastapi_utils.cbv import cbv

from api.v1.queries_params.persons import PersonSearchParams
from helpers.cache_key_builder import CACHE_EXPIRE_IN_SECONDS, key_builder
from models import Person, Film
from services.person import PersonService, get_person_service

router = APIRouter()


@cbv(router)
class PersonCBV:
    service: PersonService = Depends(get_person_service)
    response_model = Person

    @router.get("/search")
    @cache(expire=CACHE_EXPIRE_IN_SECONDS, coder=JsonCoder, key_builder=key_builder)
    async def person_list(self, params: PersonSearchParams = Depends()) -> list[Person]:
        persons = await self.service.get_list(params)
        return persons

    @router.get("/{person_id}")
    @cache(expire=CACHE_EXPIRE_IN_SECONDS, coder=JsonCoder, key_builder=key_builder)
    async def person_details(self, person_id: str) -> Person:
        person = await self.service.get_by_id(person_id)
        if not person:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="person not found"
            )
        return person

    @router.get("/{person_id}/film")
    @cache(expire=CACHE_EXPIRE_IN_SECONDS, coder=JsonCoder, key_builder=key_builder)
    async def person_films(self, person_id: str) -> list[Film]:
        films = await self.service.get_person_films(person_id)
        return films
