from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from utils.decorators import roles_required
from services.role_service import RoleService


class RoleResource(Resource):
    @jwt_required()
    @roles_required("Admin")
    def post(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "name", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        role, created = RoleService.create_role(data["name"])
        if created:
            response = jsonify({"id": str(role.id)})
            response.status = HTTPStatus.CREATED
            return response
        return {"msg": "Role is already existing"}, HTTPStatus.BAD_REQUEST

    @jwt_required()
    @roles_required("Admin")
    def get(self):
        pass

    @jwt_required()
    @roles_required("Admin")
    def put(self):
        pass

    @jwt_required()
    @roles_required("Admin")
    def delete(self):
        pass


