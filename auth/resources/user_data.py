import json

from flask_restful import Resource

from services.user_ids import UserIdsService
from utils.namespaces.profile import user
from utils.namespaces.user_data import ns, user_ids, user_ids_model


@ns.route("")
class UserPersonalData(Resource):
    @ns.marshal_list_with(user)
    @ns.expect(user_ids_model)
    def post(self) -> list[dict]:
        """Get personal data by user ids"""
        data = user_ids.parse_args()
        user_ids_data = data["user_ids"]
        response = UserIdsService.get_user_personal_data(user_ids_data)
        return response
