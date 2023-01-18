from flask_restx import reqparse

register_data = reqparse.RequestParser()
register_data.add_argument("login", type=str, required=True)
register_data.add_argument("password", type=str, required=True)
register_data.add_argument("password_confirmation", type=str, required=True)
register_data.add_argument("email", type=str, required=False)
