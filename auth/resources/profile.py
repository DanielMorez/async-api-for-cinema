from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from services.user_service import UserService
from utils.token import check_if_token_in_blacklist


class ChangePassword(Resource):
    @jwt_required()
    @check_if_token_in_blacklist()
    def post(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "password", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        user_id = get_jwt_identity()
        payload, status = UserService.change_password(user_id, data["password"])
        return payload, status


class ChangeLogin(Resource):
    @jwt_required()
    @check_if_token_in_blacklist()
    def post(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "login", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        user_id = get_jwt_identity()
        payload, status = UserService.change_login(user_id, data["login"])
        return payload, status


class Profile(Resource):
    @jwt_required()
    @check_if_token_in_blacklist()
    def get(self):
        user_id = get_jwt_identity()
        # TODO: get profile info
        return jsonify(user_id)

    @jwt_required()
    @check_if_token_in_blacklist()
    def put(self):
        user_id = get_jwt_identity()
        # TODO: update profile info
        return jsonify(user_id)
