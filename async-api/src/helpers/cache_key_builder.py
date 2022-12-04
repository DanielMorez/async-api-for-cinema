import re
from typing import Callable

from fastapi_cache import FastAPICache

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


def key_builder(
    func: Callable,
    *args,
    **kwargs,
) -> str:
    def exclude_keys(dictionary):
        params = {}
        for key, value in dictionary.items():
            if key == "kwargs":
                # удаляем ссылку на объект self из имени ключа в redis
                value = re.sub(r"<.*>", "<>", str(dictionary.get(key, None)))
            params[key] = value
        return params

    prefix = FastAPICache.get_prefix()
    cache_key = (
        f"{prefix}:{func.__module__}:{func.__name__}:{args}:{exclude_keys(kwargs)}"
    )
    return cache_key
