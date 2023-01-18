from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from services.user_role_service import UserRoleService
from utils.namespaces.roles import role
from utils.namespaces.user_role import ns
from utils.parsers.auth import access_token_required
from utils.decorators import roles_required


@ns.route("/")
@ns.expect(access_token_required)
class UserRoleResource(Resource):
    @jwt_required()
    @roles_required("Admin")
    def post(self):
        """Assign role to user"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "user_id", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "role_id", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        UserRoleService.set_user_role(data["user_id"], data["role_id"])
        return jsonify(succes=True)

    @jwt_required()
    @roles_required("Admin")
    def delete(self):
        """Remove role from user"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "user_id", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "role_id", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        UserRoleService.remove_user_role(data["user_id"], data["role_id"])
        return jsonify(succes=True)

    @ns.marshal_list_with(role)
    @jwt_required()
    @roles_required("Admin")
    def get(self):
        """Get list of user rights"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "user_id", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        roles = UserRoleService.get_user_roles(data["user_id"])
        return jsonify(roles)
