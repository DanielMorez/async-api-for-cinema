import names


test_register_post = [
    (
        {"login": names.get_last_name(), "password": "1234", "password_confirmation": "1234"},
        {"body": ["access_token", "refresh_token"]},
    )
]

test_refresh_post = [({"login": "admin", "password": "1234"}, {"body": ["access_token", "refresh_token"]})]

test_login_post = [({"login": "admin", "password": "1234"}, {"body": ["access_token", "refresh_token"]})]


test_roles_get = [({"login": "admin", "password": "1234"}, {})]
