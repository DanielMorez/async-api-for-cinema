from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
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
        user = UserService.get_user_profile(user_id)
        return jsonify(user.as_dict)

    @jwt_required()
    @check_if_token_in_blacklist()
    def patch(self):
        user_id = get_jwt_identity()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("first_name", required=False)
        self.parser.add_argument("last_name", required=False)
        self.parser.add_argument("email", required=False)
        data = self.parser.parse_args()
        user = UserService.update_user_profile(user_id, **data)
        if user:
            return jsonify(user.as_dict)
        return {"message": "Set first_name or last_name or email"}, HTTPStatus.BAD_REQUEST
