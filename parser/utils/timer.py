import functools
import time
from typing import Callable


def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f'Функция {func.__name__} выполнялась {end - start:.4f} секунд')
        return result

    return wrapper
