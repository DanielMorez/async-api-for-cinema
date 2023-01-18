from http import HTTPStatus
from flask import jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask_restful import Resource, reqparse

from services.user_service import UserService, JWTs
from utils.namespaces import registration, login, refresh, logout
from utils.namespaces.login import tokens
from utils.parsers.auth import access_token_required, refresh_token_required
from utils.parsers.login import credentials
from utils.parsers.registration import register_data
from utils.token import check_if_token_in_blacklist


@registration.ns.route("")
@registration.ns.expect(register_data)
class Registration(Resource):
    @registration.ns.marshal_with(tokens, code=HTTPStatus.CREATED)
    def post(self):
        """Register user"""
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


@login.ns.route("")
@login.ns.expect(credentials)
class Authorization(Resource):
    @login.ns.marshal_with(tokens)
    def post(self):
        """Authorization by credentials"""
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


@refresh.ns.route("")
@refresh.ns.expect(refresh_token_required)
class RefreshToken(Resource):
    @refresh.ns.marshal_with(tokens)
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


@logout.ns.route("")
@logout.ns.expect(access_token_required)
class Logout(Resource):
    @jwt_required(verify_type=False)
    @check_if_token_in_blacklist()
    def post(self):
        user_id = get_jwt_identity()
        payload = get_jwt()
        payload, status = UserService.logout(user_id, payload)
        return payload, status
