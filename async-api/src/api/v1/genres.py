from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from models import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


# Внедряем GenreService с помощью Depends(get_genre_service)
@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        # Если жанр не найден, отдаём 404 статус
        # Желательно пользоваться уже определёнными HTTP-статусами, которые содержат enum
                # Такой код будет более поддерживаемым
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    # Перекладываем данные из models.Genre в Genre
    return Genre(id=genre.id, name=genre.name)
