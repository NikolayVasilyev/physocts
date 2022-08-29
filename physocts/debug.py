"""
file: debug.py
author: Nikolay S. Vasil'ev
description: some debug tools
"""
from time import time
from typing import Any

from . import simple_log


def dbg(*x: Any, the_locals=None, the_globals=None):

    from pprint import pprint
    from types import SimpleNamespace

    the_locals = the_locals or {}
    the_globals = the_globals or {}

    lcls = SimpleNamespace(**the_locals)
    glbls = SimpleNamespace(**the_globals)

    breakpoint()  # pylint: disable=W1515

    return x


def with_time_measure(f, *a, **k):

    with simple_log.enabled():
        t = time()
        res = f(*a, **k)
        simple_log.info(f"Time elapsed: {time() - t}")

        return res
