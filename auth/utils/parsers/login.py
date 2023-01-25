from flask_restx import reqparse

credentials = reqparse.RequestParser()
credentials.add_argument("login", type=str, required=True, location="json")
credentials.add_argument("password", type=str, required=True, location="json")
