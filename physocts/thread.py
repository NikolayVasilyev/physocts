"""
file: thread.py
author: Nikolay S. Vasil'ev
description: routines for executing code in a separate thread
"""

from functools import wraps
from threading import Thread
from concurrent.futures import Future
from enum import Enum

from .log import get_logger
from .wrappers import wrap_in_either

LOG = get_logger()


class ThreadHandlerError(Exception):
    """a handler raised an exception while been executed in a separate thread"""


class FutureState(Enum):
    """future object states"""

    UNKNOWN = "unknown"
    RUNNING = "running"
    SUCCEED = "succeed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    def __str__(self):
        return self.value



def get_future_status(ftr: Future):
    """return the future object status"""

    if ftr.cancelled():
        return FutureState.CANCELLED

    if ftr.done():
        if ftr.exception() is None:
            return FutureState.SUCCEED

        return FutureState.FAILED

    if ftr.running():
        return FutureState.RUNNING

    return FutureState.UNKNOWN



def thread_executable(f):
    """
    Prepare a callable to be executed in a separate thread;
    executes a callable in safe mode and logs the results
    """

    @wraps(f)
    def g(*a, **k):

        if not (res := wrap_in_either(f)(*a, **k)):
            LOG.error("Promise handler failed: %s", res.value)
            raise ThreadHandlerError(f"handler: {f}, arguments: {a}, {k}")

        LOG.debug("Promise handler returned: %s", res.value)

    return g


def unsafe_with_timeout(timeout, exception=TimeoutError):

    def wrapper(f):

        @wraps(f)
        def g(*a, **k):

            t = Thread(
                target=f,
                args=a,
                kwargs=k)
            t.start()
            t.join(timeout)
            if t.is_alive():
                msg = f"Timeout reached for function {f.__name__} call with arguments {a}, {k}"
                LOG.error(msg)
                raise exception(msg)


        return g

    return wrapper
