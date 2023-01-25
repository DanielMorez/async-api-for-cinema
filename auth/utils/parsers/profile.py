from flask_restx import reqparse

parser = reqparse.RequestParser()
parser.add_argument("first_name", type=str, required=True, location="json")
parser.add_argument("last_name", type=str, required=True, location="json")
parser.add_argument("email", type=str, required=True, location="json")
