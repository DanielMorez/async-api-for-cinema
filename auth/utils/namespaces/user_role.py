from flask_restx import Namespace
from flask_restx import reqparse

ns = Namespace("User roles", description="User role management")

role_id_and_user_id = reqparse.RequestParser()
role_id_and_user_id.add_argument("role_id", type=str, required=True, location="json")
role_id_and_user_id.add_argument("user_id", type=str, required=True, location="json")

user_id = reqparse.RequestParser()
user_id.add_argument("user_id", type=str, required=True, location="values")
