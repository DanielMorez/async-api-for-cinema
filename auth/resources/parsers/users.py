from flask_restful import reqparse

user_filter_parser = reqparse.RequestParser()
user_filter_parser.add_argument("has_email", default=False, required=False)
user_filter_parser.add_argument("is_subscriber", default=False, required=False)
