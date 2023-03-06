from http import HTTPStatus
from typing import List

from core.exceptions import NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.user import AbstractUserService, get_user_service

user_router = APIRouter()
category_router = APIRouter()


class UserInfo(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    promo_agree: bool
    category: str
    films_month_count: int
    favourite_genre: str


class UsersInfo(BaseModel):
    users: List[UserInfo]


@user_router.get(
    '/{user_id}',
    response_model=UserInfo,
    summary="Информация по пользователю",
    description="Полная информация по пользователю по его ID",
    response_description="Информация о пользователе"
)
async def get_user(
        user_id: str,
        user_service: AbstractUserService = Depends(get_user_service)
) -> UserInfo:
    try:
        user = await user_service.get_by_id(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.error)

    return UserInfo(**user.dict())


@category_router.get(
    '/{category}',
    response_model=UsersInfo,
    summary="Список пользователей в категории",
    description="Полный список пользователей, состоящих в переданной категории",
    response_description="Список пользователей"
)
async def get_user_by_categories(
        category: str,
        user_service: AbstractUserService = Depends(get_user_service)
) -> UsersInfo:
    result = await user_service.get_by_category(category)
    users = [UserInfo(**user.dict()) for user in result]
    return UsersInfo(users=users)
