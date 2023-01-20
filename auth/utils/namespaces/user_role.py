from flask_restx import Namespace
from flask_restx import reqparse

ns = Namespace("User roles", description="User role management")

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True, location="json")
