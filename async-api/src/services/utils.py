import json


async def get_key_by_args(*args, **kwargs) -> str:
    return f'{args}:{json.dumps({"kwargs": kwargs}, sort_keys=True)}'
