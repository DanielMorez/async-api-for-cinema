from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from fastapi_utils.cbv import cbv

from api.v1.queries_params.films import FilmListParams, FilmQueryParams
from helpers.detail_messages import DETAILS
from models import Film
from services.film import FilmService, get_film_service

router = APIRouter()


@cbv(router)
class FilmCBV:
    service: FilmService = Depends(get_film_service)
    response_model = Film

    @router.get(
        "/",
        description="Get the list of films",
        summary="The list of films",
        response_description="The list of films",
        tags=["films"],
    )
    @cache()
    async def film_list(self, params: FilmListParams = Depends()) -> list[Film]:
        """
        Returns list of films sorted by imdb_rating: desc.
        """
        films = await self.service.get_list(params)
        return films

    @router.get(
        "/search",
        description="Search for films by keywords",
        summary="Film's search by keywords",
        response_description="Film's data according to keywords",
        tags=["films"],
    )
    @cache()
    async def search_film(self, params: FilmQueryParams = Depends()) -> list[Film]:
        """
        Returns list of films filtered by specified params (genre, title).
        """
        films = await self.service.search(params)
        return films

    @router.get(
        "/{film_id}",
        description="Get film's data by id",
        summary="Film's data",
        response_description="Film's data",
        tags=["films"],
    )
    @cache()
    async def film_details(self, film_id: str) -> Film:
        """
        Returns the dict with all information about the film by ID.
        """
        film = await self.service.get_by_id(film_id)
        if not film:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=DETAILS["not_found"]
            )
        return film
