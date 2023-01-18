import datetime
import logging
import uuid

from http import HTTPStatus
from uuid import UUID

import jwt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from flask_restful import abort
from pydantic import BaseModel
from sqlalchemy.exc import DataError

from config import settings
from models.user import User
from models.login_history import LoginHistory
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
        cls, login: str, password: str, password_confirmation: str, email: str = None, *args, **kwargs
    ) -> (dict, int):
        if User.find_by_login(login):
            return {"message": "User with login {} already exists".format(login)}, HTTPStatus.BAD_REQUEST

        if email:
            if User.find_by_email(email):
                return {"message": "User with email {} already exists".format(email)}, HTTPStatus.BAD_REQUEST

        if password != password_confirmation:
            return {"message": "Passwords do not match"}, HTTPStatus.BAD_REQUEST

        new_user = User(login=login, password=password, email=email)
        try:
            new_user.save()
            tokens: JWTs = cls.get_tokens(new_user)
            # TODO: notification about register
            return tokens.dict(), HTTPStatus.CREATED
        except Exception as error:
            logger.error(error)
            return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR

    @classmethod
    def login(cls, login, password, user_agent: str = None, device: str = None):
        user = User.find_by_login(login)
        if not user:
            return {"message": "User with login {} does not exist".format(login)}, HTTPStatus.BAD_REQUEST

        is_correct_password = user.verify_password(password)

        if not is_correct_password:
            return {"message": "Password is incorrect"}, HTTPStatus.FORBIDDEN

        tokens: JWTs = cls.get_tokens(user)

        jti_access_token = uuid.UUID(jwt.decode(tokens.access_token, options={"verify_signature": False})["jti"])
        jti_refresh_token = uuid.UUID(jwt.decode(tokens.refresh_token, options={"verify_signature": False})["jti"])

        login = LoginHistory(
            user_id=user.id,
            jti_access_token=jti_access_token,
            jti_refresh_token=jti_refresh_token,
            user_agent=user_agent,
            device=device,
        )
        login.save()
        # TODO: notification about authorization

        return tokens, HTTPStatus.OK

    @classmethod
    def refresh(cls, user_id: UUID, token: dict):
        user = get_user_or_error(user_id)
        tokens: JWTs = cls.get_tokens(user)
        block_token(token["jti"], token["exp"])
        save_token_updated_at = LoginHistory.save_token_updated_at(token['jti'])
        return tokens, HTTPStatus.OK

    @classmethod
    def logout(cls, user_id: UUID, token: dict) -> (dict, HTTPStatus):
        user = get_user_or_error(user_id)
        block_token(token["jti"], token["exp"])
        return {"msg": "Token successfully revoked"}, HTTPStatus.OK

    @classmethod
    def logout_from_all_devices(cls, tokens: list) -> (dict, HTTPStatus):
        for token in tokens:
            block_token(token["jti"], token["exp"])
        return {"Tokens successfully revoked": tokens}, HTTPStatus.OK

    @classmethod
    def get_tokens_from_login_histories(cls, user_id: UUID) -> list:
        user = get_user_or_error(user_id)
        login_histories = LoginHistory.get_sessions_with_date(user_id)
        tokens_histories = []
        for session in login_histories:
            tokens_histories.append(
                {
                    "jti": str(session.jti_access_token),
                    "exp": cls.exp_calculate(session.token_updated_at, "access_token"),
                }
            )
            tokens_histories.append(
                {
                    "jti": str(session.jti_refresh_token),
                    "exp": cls.exp_calculate(session.token_updated_at, "refresh_token"),
                }
            )
        return tokens_histories

    @classmethod
    def exp_calculate(cls, token_updated_at: datetime, token_type: str, timedelta=None) -> int:
        if not timedelta:
            if token_type == "access_token":
                timedelta = settings.jwt_access_token_expires
            elif token_type == "refresh_token":
                timedelta = settings.jwt_refresh_token_expires
        exp = round((token_updated_at + datetime.timedelta(seconds=timedelta)).timestamp())
        return exp

    @classmethod
    def change_password(cls, user_id: UUID, password: str) -> (dict, HTTPStatus):
        user = get_user_or_error(user_id)
        user.set_password(password)
        return {"msg": "Password was successfully changed"}, HTTPStatus.OK

    @classmethod
    def change_login(cls, user_id: UUID, login: str) -> (dict, HTTPStatus):
        user = get_user_or_error(user_id)
        user.set_password(login)
        return {"msg": "Login was successfully changed"}, HTTPStatus.OK

    @classmethod
    def get_login_histories(cls, user_id: UUID) -> list:
        login_histories = LoginHistory.get_sessions(user_id)
        return [obj.serialize() for obj in login_histories]

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
