"""
file: debug.py
author: Nikolay S. Vasil'ev
description: some debug tools
"""
from time import time
from typing import Any

from . import simple_log


def dbg(x: Any):
    breakpoint()  # pylint: disable=W1515
    return x

def with_time_measure(f, *a, **k):

    with simple_log.enabled():
        t = time()
        res = f(*a, **k)
        simple_log.info(f"Time elapsed: {time() - t}")

        return res
