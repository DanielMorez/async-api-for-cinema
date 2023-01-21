import names

admin_authorization = {"login": "pytest_superuser", "password": "123456"}

login_authorization = {"login": f"pytest_{names.get_last_name()}", "password": "123456"}

test_register_post = [
    (
        {
            "login": login_authorization["login"],
            "password": login_authorization["password"],
            "password_confirmation": login_authorization["password"],
        },
        {"body": ["access_token", "refresh_token"]},
    )
]

test_refresh_post = [(login_authorization, {"body": ["access_token", "refresh_token"]})]

test_login_post = [(login_authorization, {"body": ["access_token", "refresh_token"]})]

test_roles_get = [(login_authorization, {})]

test_roles_put = [({"id": "052269a3-25b6-4b86-84b3-5c484a550bb5", "name": "admin"}, {})]
