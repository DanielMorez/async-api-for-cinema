import uuid
from http import HTTPStatus

from flask_restful import Resource
from flask_restx import fields

from resources.parsers.users import user_filter_parser
from services.user_ids import UserIdsService
from utils.namespaces.user_filters import ns, user_filters


@ns.route("")
class UserIds(Resource):
    @ns.response(
        HTTPStatus.OK,
        "Success",
        fields.List(fields.String(example=str(uuid.uuid4())))
    )
    @ns.expect(user_filters)
    def post(self) -> list[str]:
        """Get list of user ids"""
        data = user_filter_parser.parse_args()
        user_ids = UserIdsService.get_user_ids(data)
        return user_ids
