from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv

from api.v1.queries_params.genres import GenreListParams
from models import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@cbv(router)
class PersonCBV:
    service: GenreService = Depends(get_genre_service)
    response_model = Genre

    @router.get('/list')
    async def person_list(self, params: GenreListParams = Depends()) -> list[Genre]:
        genres = await self.service.get_list(params)
        return genres

    @router.get('/{genre_id}')
    async def film_details(self, person_id: str) -> Genre:
        genre = await self.service.get_by_id(person_id)
        if not genre:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
        return genre
