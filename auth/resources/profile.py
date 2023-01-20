from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from resources.parsers.profile import change_password, change_login, change_profile
from services.user_service import UserService
from utils.namespaces.profile import ns, user, login, password
from utils.parsers.auth import access_token_required
from utils.parsers.profile import parser
from utils.token import check_if_token_in_blacklist


@ns.route("/change-password")
@ns.expect(access_token_required, password)
class ChangePassword(Resource):
    @jwt_required()
    @check_if_token_in_blacklist()
    def post(self):
        """Change password"""
        data = change_password.parse_args()
        user_id = get_jwt_identity()
        payload, status = UserService.change_password(user_id, data["password"])
        return payload, status


@ns.route("/change-login")
@ns.expect(access_token_required, login)
class ChangeLogin(Resource):
    @jwt_required()
    @check_if_token_in_blacklist()
    def post(self):
        """Change login"""
        data = change_login.parse_args()
        user_id = get_jwt_identity()
        payload, status = UserService.change_login(user_id, data["login"])
        return payload, status


@ns.route("")
@ns.expect(access_token_required)
class Profile(Resource):
    @ns.marshal_with(user)
    @jwt_required()
    @check_if_token_in_blacklist()
    def get(self):
        """Get user profile"""
        user_id = get_jwt_identity()
        user_instance = UserService.get_user_profile(user_id)
        return user_instance.as_dict

    @ns.marshal_with(user)
    @ns.expect(parser)
    @jwt_required()
    @check_if_token_in_blacklist()
    def patch(self):
        """Change first or last names or email"""
        user_id = get_jwt_identity()
        data = change_profile.parse_args()
        user_instance = UserService.update_user_profile(user_id, **data)
        return user_instance.as_dict
