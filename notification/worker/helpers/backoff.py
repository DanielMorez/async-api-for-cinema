import time
import logging

from functools import wraps
from typing import Any

logger = logging.getLogger(__name__)


def backoff(
        start_sleep_time: float | int = 0.1,
        factor: int = 2,
        border_sleep_time: float | int = 10
):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени
    повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                logger.error(f'Failed {func.__name__} with {str(error)}')
                n = waiting = 0
                while True:
                    try:
                        return func(*args, **kwargs)
                    except Exception as error:
                        logger.error(f'Failed {func.__name__} with {str(error)}')
                        if waiting < border_sleep_time:
                            n += 1
                            waiting = start_sleep_time * factor ** n
                        time.sleep(waiting)
        return inner

    return func_wrapper


def reconnect(func) -> Any:
    """ Reconnect to client on failure."""
    @wraps(func)
    def wrapper(client, *args, **kwargs):
        if not client.is_connected:
            logger.warning(f"Lost connection to client: `{client}`. Trying to establish new connection...")
            client.reconnect()

        return func(client, *args, **kwargs)

    return wrapper
