from flask_restful import reqparse

change_password = reqparse.RequestParser()
change_password.add_argument(
    "password", help="This field cannot be blank", required=True
)

change_login = reqparse.RequestParser()
change_login.add_argument("login", help="This field cannot be blank", required=True)

change_profile = reqparse.RequestParser()
change_profile.add_argument("first_name", required=False)
change_profile.add_argument("last_name", required=False)
change_profile.add_argument("email", required=False)

delete_profile = reqparse.RequestParser()
delete_profile.parser = reqparse.RequestParser()
delete_profile.add_argument("user_id", help="This field cannot be blank", required=True)
