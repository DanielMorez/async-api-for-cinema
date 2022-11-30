from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from models.genre import Genre
from models.person import Person
from models.base_model import PyBaseModel
from services.film import FilmService, get_film_service

router = APIRouter()


class FilmListAPI(PyBaseModel, BaseModel):
    title: str
    imdb_rating: float
    genre: list[Genre]


class FilmAPI(PyBaseModel, BaseModel):
    title: str
    imdb_rating: float
    description: str
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]


@router.get('/',
            response_model=list[FilmListAPI],
            response_description='List of films')
async def film_list(
    page_size: int = Query(10, description='Number of films on page'),
    page: int = Query(1, description='Page number'),
    sort: str = Query('', description='Sorting fields (A comma-separated list '
                                      'of "field":"direction(=asc|desc)" '
                                      'pairs. Example: imdb_rating:desc)'),
    genre: str = Query(None, description='Filter by genre uuid'),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmListAPI]:
    """
    Returns list of films by the parameters specified in the query.
    Each element of the list is a dict of the FilmListAPI structure.
    """
    films = await film_service.all(page_size=page_size, page=page, sort=sort, genre=genre)
    return [FilmListAPI.parse_obj(film.dict(by_alias=True)) for film in films]


@router.get('/search',
            response_model=list[FilmListAPI],
            response_description='List of films')
async def film_search(
    page_size: int = Query(10, description='Number of films on page'),
    page: int = Query(1, description='Page number'),
    sort: str = Query('', description='Sorting fields (A comma-separated list '
                                      'of "field":"direction(=asc|desc)" '
                                      'pairs. Example: imdb_rating:desc)'),
    query: str = Query(None, description='Part of the movie title (Example: dark sta )'),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmListAPI]:
    """
    Returns list of films by the parameters specified in the query.
    Each element of the list is a dict of the FilmListAPI structure.

    Unlike the /films/ endpoint, it contains the "query" parameter.

    Parameter **query**: part of film title.
    """
    films = await film_service.all(page_size=page_size, page=page, sort=sort, query=query)
    return [FilmListAPI.parse_obj(film.dict(by_alias=True)) for film in films]


@router.get('/{film_id}',
            response_model=FilmAPI,
            response_description='Dict with all information about the film')
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmAPI:
    """
    Returns the dict with all information about the film by ID.
    """
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmAPI(**film.dict(by_alias=True))
