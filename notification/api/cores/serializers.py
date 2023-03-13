import json
from uuid import UUID

from orjson import orjson


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return string
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def json_serializer(data):
    return json.dumps(data, cls=UUIDEncoder).encode()


def json_deserializer(data):
    return json.loads(data.decode())


def orjson_dumps(v, *, default) -> str:
    return orjson.dumps(v, default=default).decode()
