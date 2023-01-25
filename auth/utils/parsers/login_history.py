from flask_restx import reqparse

expect_page = reqparse.RequestParser()
expect_page.add_argument("page", type=int, location="values")
expect_page.add_argument("page_size", type=int, location="values")
