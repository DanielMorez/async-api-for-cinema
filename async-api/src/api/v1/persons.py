from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from fastapi_utils.cbv import cbv

from api.v1.queries_params.persons import PersonSearchParams
from helpers.detail_messages import DETAILS
from models import Person, Film
from services.person import PersonService, get_person_service

router = APIRouter()


@cbv(router)
class PersonCBV:
    service: PersonService = Depends(get_person_service)
    response_model = Person

    @router.get(
        "/search",
        description="Search for persons by keywords",
        summary="Person's search by keywords",
        response_description="Person's data according to keywords",
        tags=["persons"],
    )
    @cache()
    async def person_list(self, params: PersonSearchParams = Depends()) -> list[Person]:
        """
        Returns list of persons filtered by specified params (gender, name).
        """
        persons = await self.service.get_list(params)
        return persons

    @router.get(
        "/{person_id}",
        description="Get person's data by id",
        summary="Person's data",
        response_description="Person's data",
        tags=["persons"],
    )
    @cache()
    async def person_details(self, person_id: str) -> Person:
        """
        Returns the dict with all information about the person by ID.
        """
        person = await self.service.get_by_id(person_id)
        if not person:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=DETAILS["not_found"]
            )
        return person

    @router.get(
        "/{person_id}/film",
        description="Search for films by person's id",
        summary="Films by person's id",
        response_description="The list of films by person's id",
        tags=["persons"],
    )
    @cache()
    async def person_films(self, person_id: str) -> list[Film]:
        """
        Returns list of films by specified person_id.
        """
        films = await self.service.get_person_films(person_id)
        return films
