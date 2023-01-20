from flask_restful import reqparse

set_or_delete = reqparse.RequestParser()
set_or_delete.add_argument("user_id", help="This field cannot be blank", required=True)
set_or_delete.add_argument("role_id", help="This field cannot be blank", required=True)

user_id_parser = reqparse.RequestParser()
user_id_parser.add_argument(
    "user_id", help="This field cannot be blank", required=True, location="values"
)
