"""
file: debug.py
author: Nikolay S. Vasil'ev
description: some debug tools
"""
from time import time

from . import simple_log


def dbg(x):
    breakpoint()
    return x

def with_time_measure(f, *a, **k):
    with simple_log.with_enabled_info():
        t = time()
        res = f(*a, **k)
        simple_log.info(f"Time elapsed: {time() - t}")

        return res
