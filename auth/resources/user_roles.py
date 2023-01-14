from http import HTTPStatus

from flask import jsonify, abort
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from utils.decorators import roles_required
from services.user_role_service import UserRoleService


class UserRolesResource(Resource):
    @jwt_required()
    @roles_required("Admin")
    def post(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "user_id", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "role_id", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        users_role, created = UserRoleService.create_user_roles(data["user_id"], data["role_id"])
        if created:
            response = jsonify({"id": str(users_role.id)})
            response.status = HTTPStatus.CREATED
            return response
        return {"msg": "Users_role already exists"}, HTTPStatus.BAD_REQUEST

    @jwt_required()
    @roles_required("Admin")
    def delete(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
                "role_id", help="This field cannot be blank", required=True
            )
        self.parser.add_argument(
                "user_id", help="This field cannot be blank", required=True
            )
        data = self.parser.parse_args()
        #user_id = get_jwt_identity()
        payload, status = UserRoleService.remove_users_role(data["user_id"], data["role_id"])
        return payload, status
