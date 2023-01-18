from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from utils.decorators import roles_required
from services.role_service import RoleService
from utils.namespaces.roles import ns, role
from utils.parsers.auth import access_token_required


@ns.route("/")
@ns.expect(access_token_required)
class RoleResource(Resource):
    @ns.marshal_with(role, code=HTTPStatus.CREATED)
    @jwt_required()
    @roles_required("Admin")
    def post(self):
        """Create role"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "name", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        role, created = RoleService.create_role(data["name"])
        if created:
            response = jsonify({"id": str(role.id), "name": role.name})
            response.status = HTTPStatus.CREATED
            return response
        return {"msg": "Role already exists"}, HTTPStatus.BAD_REQUEST

    @ns.marshal_list_with(role)
    @jwt_required()
    @roles_required("Admin")
    def get(self):
        """Get list of roles"""
        roles = RoleService.get_roles()
        return jsonify(roles)

    @jwt_required()
    @roles_required("Admin")
    def put(self):
        """Change role"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("id", help="This field cannot be blank", required=True)
        self.parser.add_argument(
            "name", help="This field cannot be blank", required=True
        )
        data = self.parser.parse_args()
        RoleService.update(data["id"], data["name"])
        return jsonify(success=True)

    @jwt_required()
    @roles_required("Admin")
    def delete(self):
        """Delete role"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("id", help="This field cannot be blank", required=True)
        data = self.parser.parse_args()
        RoleService.delete(data["id"])
        return jsonify(success=True)
