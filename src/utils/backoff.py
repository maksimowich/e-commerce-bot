from functools import wraps
import time

from loguru import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, max_attempts=7):
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            attempts = 0

            while attempts < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.info(
                        f"Error occurred: {e}. "
                        f"Retrying in {sleep_time:.2f} seconds... (Attempt {attempts}/{max_attempts})"
                    )
                    time.sleep(sleep_time)
                    sleep_time = min(sleep_time * factor, border_sleep_time)

        return inner

    return func_wrapper
