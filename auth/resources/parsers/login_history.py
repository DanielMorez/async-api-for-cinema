from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument("page", type=int, location="values")
parser.add_argument("page_size", type=int, location="values")
