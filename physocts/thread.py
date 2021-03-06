"""
file: thread.py
author: Nikolay S. Vasil'ev
description: routines for executing code in a separate thread
"""

from functools import wraps
from threading import Thread

from .log import get_logger
from .wrappers import wrap_in_either

LOG = get_logger()


def thread_executable(f):
    """
    Prepare a callable to be executed in a separate thread;
    executes a callable in safe mode and logs the results
    """

    @wraps(f)
    def g(*a, **k):

        if not (res := wrap_in_either(f)(*a, **k)):
            LOG.error("Promise handler failed: %s", res.value)
        else:
            LOG.debug("Promise handler returned: %s", res.value)

    return g


def unsafe_with_timeout(timeout):

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
                raise TimeoutError(f"Timeout reached for function {f} call with arguments {a}, {k}")


        return g

    return wrapper
