from http import HTTPStatus

from flask import jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse
from sqlalchemy.exc import NoResultFound

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
        return {"msg": "Role already exists"}, HTTPStatus.BAD_REQUEST

    @jwt_required()
    @roles_required("Admin")
    def get(self):
        roles = get_jwt()
        return jsonify(roles)

    @jwt_required()
    @roles_required("Admin")
    def put(self):
        role_id = get_jwt_identity()
        # TODO: update role info
        return jsonify(role_id)

    @jwt_required()
    @roles_required("Admin")
    def delete(self):
        try:
            role_id = get_jwt_identity()
            return jsonify(role_id)
        except NoResultFound:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, {"msg": "Something went wrong"})
