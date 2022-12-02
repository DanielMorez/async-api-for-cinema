from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv

from api.v1.queries_params.films import FilmListParams
from models import Film
from services.film import FilmService, get_film_service

router = APIRouter()


@cbv(router)
class FilmCBV:
    service: FilmService = Depends(get_film_service)
    response_model = Film

    @router.get('/list')
    async def film_list(self, params: FilmListParams = Depends()) -> list[Film]:
        films = await self.service.get_list(params)
        return films

    @router.get('/{film_id}')
    async def film_details(self, film_id: str) -> Film:
        film = await self.service.get_by_id(film_id)
        if not film:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
        return film
