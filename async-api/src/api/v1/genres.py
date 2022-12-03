from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache import JsonCoder
from fastapi_cache.decorator import cache
from fastapi_utils.cbv import cbv

from api.v1.queries_params.genres import GenreListParams
from helpers.cache_key_builder import CACHE_EXPIRE_IN_SECONDS, key_builder
from models import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@cbv(router)
class GenreCBV:
    service: GenreService = Depends(get_genre_service)
    response_model = Genre

    @router.get('/list')
    @cache(expire=CACHE_EXPIRE_IN_SECONDS, coder=JsonCoder, key_builder=key_builder)
    async def genre_list(self, params: GenreListParams = Depends()) -> list[Genre]:
        genres = await self.service.get_list(params)
        return genres

    @router.get('/{genre_id}')
    @cache(expire=CACHE_EXPIRE_IN_SECONDS, coder=JsonCoder, key_builder=key_builder)
    async def film_details(self, genre_id: str) -> Genre:
        genre = await self.service.get_by_id(genre_id)
        if not genre:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
        return genre
