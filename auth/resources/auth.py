from http import HTTPStatus
from flask import jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask_restful import Resource, reqparse

from services.user_service import UserService, JWTs
from utils.token import check_if_token_in_blacklist


class Registration(Resource):
    def post(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "login", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "password", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "password_confirmation", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "email", help="This field can be blank", required=False
        )
        data = self.parser.parse_args()
        payload, status = UserService.register(**data)
        return payload, status


class Authorization(Resource):
    def post(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "login", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "password", help="This field cannot be blank", required=True
        )
        self.parser.add_argument("User-Agent", location="headers")
        self.parser.add_argument("Device", location="headers")
        data = self.parser.parse_args()
        payload, status = UserService.login(
            data["login"], data["password"], data.get("User-Agent"), data.get("Device")
        )
        if status == HTTPStatus.OK and isinstance(payload, JWTs):
            resp = jsonify(payload.dict())
            resp.headers = {"Authorization": f"Bearer {payload.access_token}"}
            return resp
        return payload, status


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    @check_if_token_in_blacklist()
    def post(self):
        user_id = get_jwt_identity()
        refresh_token = get_jwt()
        payload, status = UserService.refresh(user_id, refresh_token)
        if status == HTTPStatus.OK and isinstance(payload, JWTs):
            resp = jsonify(payload.dict())
            resp.headers = {"Authorization": f"Bearer {payload.access_token}"}
            return resp
        return payload, status


class Logout(Resource):
    @jwt_required(verify_type=False)
    @check_if_token_in_blacklist()
    def post(self):
        user_id = get_jwt_identity()
        payload = get_jwt()
        payload, status = UserService.logout(user_id, payload)
        return payload, status
