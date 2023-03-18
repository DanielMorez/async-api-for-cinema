from flask_restx import Namespace
from flask_restx import reqparse

ns = Namespace("User filters", description="Using by notification service")

user_filters = reqparse.RequestParser()
user_filters.add_argument("has_email", type=bool, required=False, location="json")
user_filters.add_argument("is_subscriber", type=bool, required=False, location="json")

