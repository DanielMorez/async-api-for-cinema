from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from utils.decorators import roles_required
from services.user_role_service import UserRoleService


class UserRoleResource(Resource):
    @jwt_required()
    @roles_required("Admin")
    def put(self):
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
