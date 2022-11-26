from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from models import Person
from services.person import PersonService, get_person_service

router = APIRouter()


# Внедряем PersonService с помощью Depends(get_person_service)
@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        # Если персона не найдена, отдаём 404 статус
        # Желательно пользоваться уже определёнными HTTP-статусами, которые содержат enum
                # Такой код будет более поддерживаемым
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    # Перекладываем данные из models.Person в {Person}
    return Person(id=person.id, last_name=person.last_name, first_name=person.first_name)
