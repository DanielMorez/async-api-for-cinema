from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv

from api.v1.queries_params.persons import PersonListParams
from models import Person
from services.person import PersonService, get_person_service

router = APIRouter()


@cbv(router)
class PersonCBV:
    service: PersonService = Depends(get_person_service)
    response_model = Person

    @router.get('/list')
    async def person_list(self, params: PersonListParams = Depends()) -> list[Person]:
        persons = await self.service.get_list(params)
        return persons

    @router.get('/{person_id}')
    async def film_details(self, person_id: str) -> Person:
        person = await self.service.get_by_id(person_id)
        if not person:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
        return person
