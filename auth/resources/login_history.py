from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from resources.parsers.login_history import parser
from services.user_service import UserService
from utils.namespaces.login_history import ns, pagination_login_histories
from utils.parsers.auth import access_token_required
from utils.parsers.login_history import expect_page
from utils.token import check_if_token_in_blacklist


@ns.route("")
@ns.expect(access_token_required)
class LoginHistories(Resource):
    @ns.marshal_with(pagination_login_histories)
    @ns.expect(expect_page)
    @jwt_required()
    @check_if_token_in_blacklist()
    def get(self):
        """Get a list of authorizations"""
        user_id = get_jwt_identity()
        kwargs = parser.parse_args()
        login_histories = UserService.get_login_histories(user_id, **kwargs)
        return login_histories
