from flask_restx import Api


def register_models(api: Api):
    from utils.namespaces.roles import role

    api.model(*role)