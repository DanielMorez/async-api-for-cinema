from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_restful import Resource

from resources.parsers.role import role_creating, role_updating, role_deleting
from utils.decorators import roles_required
from services.role_service import RoleService
from utils.namespaces.roles import (
    ns,
    parser,
    role_id,
    role as role_response,
    role_id_and_name,
)
from utils.parsers.auth import access_token_required


@ns.route("")
# @ns.expect(access_token_required)
class RoleResource(Resource):
    @ns.expect(parser)
    @ns.marshal_with(role_response, code=HTTPStatus.CREATED)
    # @jwt_required()
    # @roles_required("Admin")
    def post(self):
        """Create role"""
        data = role_creating.parse_args()
        role, created = RoleService.create_role(data["name"])
        return role.as_dict, HTTPStatus.CREATED if created else HTTPStatus.OK

    @ns.marshal_list_with(role_response)
    # @jwt_required()
    # @roles_required("Admin")
    def get(self):
        """Get list of roles"""
        roles = RoleService.get_roles()
        return roles

    @ns.expect(role_id_and_name)
    @ns.marshal_with(role_response)
    # @jwt_required()
    # @roles_required("Admin")
    def put(self):
        """Change role"""
        data = role_updating.parse_args()
        role = RoleService.update(data["id"], data["name"])
        return role.as_dict

    @ns.expect(role_id)
    # @jwt_required()
    # @roles_required("Admin")
    def delete(self):
        """Delete role"""
        data = role_deleting.parse_args()
        RoleService.delete(data["id"])
        return {"message": "Success"}
