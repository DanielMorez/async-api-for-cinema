from flask_restful import reqparse

role_creating = reqparse.RequestParser()
role_creating.add_argument("name", help="This field cannot be blank", required=True)

role_updating = reqparse.RequestParser()
role_updating.add_argument("id", help="This field cannot be blank", required=True)
role_updating.add_argument("name", help="This field cannot be blank", required=True)

role_deleting = reqparse.RequestParser()
role_deleting.add_argument("id", help="This field cannot be blank", required=True)
