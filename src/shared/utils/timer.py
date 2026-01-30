import functools
import inspect
import time
from typing import Any, Callable, TypeVar, cast

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec  # type: ignore

from shared.utils.logger_config import setup_logger

logger = setup_logger()

P = ParamSpec("P")
R = TypeVar("R")


def time_execution(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator to log the execution time of a function.
    Supports both synchronous and asynchronous functions.
    """
    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            start_time = time.time()
            try:
                # We rely on the runtime check above to know this is awaitable
                result = await func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(
                    f"⏱️ Function '{func.__name__}' execution time: {execution_time:.4f} seconds"
                )

        return cast(Callable[P, R], async_wrapper)
    else:

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(
                    f"Function '{func.__name__}' execution time: {execution_time:.4f} seconds"
                )

        return cast(Callable[P, R], wrapper)
