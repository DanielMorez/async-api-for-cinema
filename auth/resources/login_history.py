from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from services.user_service import UserService
from utils.namespaces.login_history import ns, login_history
from utils.parsers.auth import access_token_required
from utils.token import check_if_token_in_blacklist


@ns.route("")
@ns.expect(access_token_required)
class LoginHistories(Resource):
    @ns.marshal_list_with(login_history)
    @jwt_required()
    @check_if_token_in_blacklist()
    def get(self):
        """Get a list of authorizations"""
        user_id = get_jwt_identity()
        login_histories = UserService.get_login_histories(user_id)
        return jsonify(login_histories)
