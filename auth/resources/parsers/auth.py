from flask_restful import reqparse

register_parser = reqparse.RequestParser()
register_parser.add_argument("login", help="This field cannot be blank", required=True)
register_parser.add_argument(
    "password", help="This field cannot be blank", required=True
)
register_parser.add_argument(
    "password_confirmation", help="This field cannot be blank", required=True
)
register_parser.add_argument("email", help="This field can be blank", required=False)

auth_parser = reqparse.RequestParser()
auth_parser.add_argument("login", help="This field cannot be blank", required=True)
auth_parser.add_argument("password", help="This field cannot be blank", required=True)
auth_parser.add_argument("User-Agent", location="headers")
auth_parser.add_argument("Device", location="headers")
