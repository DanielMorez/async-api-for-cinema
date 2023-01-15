from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from services.user_service import UserService
from utils.token import check_if_token_in_blacklist


class LoginHistories(Resource):
    @jwt_required()
    @check_if_token_in_blacklist()
    def get(self):
        user_id = get_jwt_identity()
        login_histories = UserService.get_login_histories(user_id)
        return jsonify(login_histories)
