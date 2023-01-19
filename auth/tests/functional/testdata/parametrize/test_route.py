test_register_post = [
    (
        {"login": "username", "password": "123", "password_confirmation": "123"},
        {"body": ["access_token", "refresh_token"]},
    )
]

test_refresh_post = [
    ({"login": "admin", "password": "123"}, {"body": ["access_token", "refresh_token"]})
]

test_login_post = [
    ({"login": "admin", "password": "123"}, {"body": ["access_token", "refresh_token"]})
]


test_roles_get = [({"login": "admin", "password": "123"}, {})]
