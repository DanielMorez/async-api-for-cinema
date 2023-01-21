import logging

from http import HTTPStatus
from uuid import UUID

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from flask import abort
from pydantic import BaseModel
from sqlalchemy.exc import DataError

from models.user import User
from models.login_history import LoginHistory

from utils.pagination import paginate
from utils.token import block_token

logger = logging.getLogger(__name__)


def get_user_or_error(user_id: UUID) -> User:
    try:
        user = User.find_by_id(user_id)
    except DataError:
        abort(HTTPStatus.BAD_REQUEST, "Invalid id")
    else:
        if not user:
            abort(HTTPStatus.FORBIDDEN, "Invalid token")
        return user


class JWTs(BaseModel):
    access_token: str
    refresh_token: str


class UserService:
    @classmethod
    def get_tokens(cls, user: User) -> JWTs:
        return JWTs(
            access_token=create_access_token(identity=user.id),
            refresh_token=create_refresh_token(identity=user.id),
        )

    @classmethod
    def register(
        cls,
        login: str,
        password: str,
        password_confirmation: str,
        email: str = None,
        *args,
        **kwargs,
    ) -> (dict, int):
        if User.find_by_login(login):
            abort(
                HTTPStatus.BAD_REQUEST,
                "User with login {} already exists".format(login),
            )

        if len(login) <= 6:
            abort(HTTPStatus.BAD_REQUEST, "Login has to contains more pr equal 6 symbols")

        if email:
            if User.find_by_email(email):
                abort(
                    HTTPStatus.BAD_REQUEST,
                    "User with email {} already exists".format(email),
                )

        if password != password_confirmation:
            abort(HTTPStatus.BAD_REQUEST, "Passwords do not match")

        if len(password) < 6:
            abort(
                HTTPStatus.BAD_REQUEST,
                "Password has to contains more pr equal 6 symbols",
            )

        new_user = User(login=login, password=password, email=email)
        try:
            new_user.save()
            tokens: JWTs = cls.get_tokens(new_user)
            # TODO: notification about register
            return tokens.dict(), HTTPStatus.CREATED
        except Exception as error:
            logger.error(error)
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

    @classmethod
    def login(cls, login: str, password: str, user_agent: str = None, device: str = None):
        user = User.find_by_login(login)
        if not user:
            abort(
                HTTPStatus.BAD_REQUEST,
                "User with login {} does not exist".format(login),
            )

        is_correct_password = user.verify_password(password)

        if not is_correct_password:
            abort(HTTPStatus.BAD_REQUEST, "Password is incorrect")

        tokens: JWTs = cls.get_tokens(user)

        login = LoginHistory(user_id=user.id, user_agent=user_agent, device=device)
        login.save()
        # TODO: notification about authorization

        return tokens, HTTPStatus.OK

    @classmethod
    def refresh(cls, user_id: UUID, token: dict):
        user = get_user_or_error(user_id)
        tokens: JWTs = cls.get_tokens(user)
        block_token(token["jti"], token["exp"])
        return tokens, HTTPStatus.OK

    @classmethod
    def logout(cls, user_id: UUID, token: dict) -> (dict, HTTPStatus):
        user = get_user_or_error(user_id)
        block_token(token["jti"], token["exp"])
        return {"message": "Token successfully revoked"}, HTTPStatus.OK

    @classmethod
    def logout_from_all_devices(cls, user_id: UUID):
        # TODO:
        #  find all active access and refresh tokens
        #  and block them
        return {"msg": "Tokens successfully revoked"}, HTTPStatus.OK

    @classmethod
    def change_password(cls, user_id: UUID, password: str) -> (dict, HTTPStatus):
        user = get_user_or_error(user_id)
        user.set_password(password)
        return {"message": "Password was successfully changed"}, HTTPStatus.OK

    @classmethod
    def change_login(cls, user_id: UUID, login: str) -> (dict, HTTPStatus):
        user = get_user_or_error(user_id)
        user.set_password(login)
        return {"message": "Login was successfully changed"}, HTTPStatus.OK

    @classmethod
    def get_login_histories(cls, user_id: UUID, page: int = 1, page_size: int = 10) -> dict:
        query = LoginHistory.get_sessions(user_id)
        data = paginate(query, page, page_size)
        return data

    @classmethod
    def get_user_profile(cls, user_id: UUID) -> User:
        user = get_user_or_error(user_id)
        return user

    @classmethod
    def update_user_profile(
        cls,
        user_id: UUID,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
    ) -> User:
        user = get_user_or_error(user_id)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email

        if email or last_name or first_name:
            user.save()
            return user
