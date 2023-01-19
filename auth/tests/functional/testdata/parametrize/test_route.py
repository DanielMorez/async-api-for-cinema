import names

test_roles_get = [
    (
        {"login": "admin", "password": "1234"},
        {"body": [
            {
                "id": "29bd2c9b-c483-4ff7-9a7d-1b79bf675792",
                "name": "admin"
            }
        ]}
    )
]

test_register_post = [
    (
        {"login": names.get_last_name(), "password": "1234", "password_confirmation": "1234"},
        {"body": ['access_token', 'refresh_token']}
    )
]

test_refresh_post = [
    (
        {"login": "admin", "password": "1234"},
        {"body": ['access_token', 'refresh_token']}
    )
]
