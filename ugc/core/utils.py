from orjson import orjson


def orjson_dumps(v, *, default) -> str:
    return orjson.dumps(v, default=default).decode()
