from flask_jwt_extended import jwt_required
from flask_restful import Resource

from resources.parsers.user_role import user_id_parser, set_or_delete
from services.user_role_service import UserRoleService
from utils.namespaces.roles import role as role_response
from utils.namespaces.user_role import ns, role_id_and_user_id, user_id
from utils.parsers.auth import access_token_required
from utils.decorators import roles_required


@ns.route("")
# @ns.expect(access_token_required)
class UserRoleResource(Resource):
    @ns.marshal_list_with(role_response)
    @ns.expect(role_id_and_user_id)
    # @jwt_required()
    # @roles_required("Admin")
    def post(self):
        """Assign role to user"""
        data = set_or_delete.parse_args()
        roles = UserRoleService.set_user_role(data["user_id"], data["role_id"])
        return roles

    @ns.marshal_with(role_response)
    @ns.expect(role_id_and_user_id)
    # @jwt_required()
    # @roles_required("Admin")
    def delete(self):
        """Remove role from user"""
        data = set_or_delete.parse_args()
        role = UserRoleService.remove_user_role(data["user_id"], data["role_id"])
        return role

    @ns.marshal_list_with(role_response)
    @ns.expect(user_id)
    # @jwt_required()
    # @roles_required("Admin")
    def get(self):
        """Get list of user rights"""
        data = user_id_parser.parse_args()
        roles = UserRoleService.get_user_roles(data["user_id"])
        return roles
