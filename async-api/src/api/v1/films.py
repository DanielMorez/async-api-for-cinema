from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_cache.decorator import cache
from fastapi_utils.cbv import cbv

from api.v1.queries_params.films import FilmListParams, FilmQueryParams
from core.config import Settings
from helpers.detail_messages import DETAILS
from models import Film
from services.film import FilmService, get_film_service

settings = Settings()

router = APIRouter()
auth_scheme = HTTPBearer()


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
    async def film_list(self, request: Request, token: HTTPAuthorizationCredentials = Depends(auth_scheme), params: FilmListParams = Depends()) -> list[Film]:
        """
        Returns list of films sorted by imdb_rating: desc.
        """
        films = await self.service.get_list(params)
        if not request.user.is_authenticated:
            for film in films:
                film.description = None
                film.imdb_rating = None
        if request.user.is_authenticated:
            if "Subscriber" not in request.user.roles:
                for film in films:
                    film.description = None
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
