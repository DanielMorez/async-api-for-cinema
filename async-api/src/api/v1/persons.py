from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache import JsonCoder
from fastapi_cache.decorator import cache
from fastapi_utils.cbv import cbv

from api.v1.queries_params.persons import PersonListParams
from helpers.cache_key_builder import CACHE_EXPIRE_IN_SECONDS, key_builder
from models import Person
from services.person import PersonService, get_person_service

router = APIRouter()


@cbv(router)
class PersonCBV:
    service: PersonService = Depends(get_person_service)
    response_model = Person

    @router.get('/list')
    @cache(expire=CACHE_EXPIRE_IN_SECONDS, coder=JsonCoder, key_builder=key_builder)
    async def person_list(self, params: PersonListParams = Depends()) -> list[Person]:
        persons = await self.service.get_list(params)
        return persons

    @router.get('/{person_id}')
    @cache(expire=CACHE_EXPIRE_IN_SECONDS, coder=JsonCoder, key_builder=key_builder)
    async def film_details(self, person_id: str) -> Person:
        person = await self.service.get_by_id(person_id)
        if not person:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
        return person
