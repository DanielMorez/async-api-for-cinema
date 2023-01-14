import json
from http import HTTPStatus

from flask import abort, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy.exc import NoResultFound

from services.role_service import RoleService
from utils.decorators import roles_required


class RoleResource(Resource):
    @jwt_required()
    @roles_required("admin")
    def post(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "name", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "can_create_update", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "can_read", help="This field cannot be blank", required=True
        )
        self.parser.add_argument(
            "can_delete", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        role, created = RoleService.create_role(
            data["name"].lower(),
            bool(json.loads(data["can_create_update"].lower())),
            bool(json.loads(data["can_read"].lower())),
            bool(json.loads(data["can_delete"].lower())),
        )
        if created:
            return {"msg": "Role created successfully"}, HTTPStatus.CREATED
        return {"msg": "Role already exists"}, HTTPStatus.BAD_REQUEST

    @jwt_required()
    @roles_required("admin")
    def get(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "name", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        role, instance = RoleService.get_role(data["name"])
        if instance:
            response = jsonify(
                {
                    "role.id": role.id,
                    "name": role.name,
                    "can_create_update": role.can_create_update,
                    "can_read": role.can_read,
                    "can_delete": role.can_delete,
                }
            )
            response.status = HTTPStatus.OK
            return response
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND

    @jwt_required()
    @roles_required("admin")
    def put(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "name", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        role_id = get_jwt_identity()
        payload, status = RoleService.update_role(role_id, data["name"])
        return payload, status

    @jwt_required()
    @roles_required("admin")
    def delete(self):
        role_id = get_jwt_identity()
        payload, status = RoleService.remove_role(role_id)
        return payload, status
