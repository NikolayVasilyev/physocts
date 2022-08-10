"""
file: _list.py
author: Nikolay S. Vasil'ev
description: a set of functions for handling with instances that have
    `__getitem__` and `__getitem__` methods; all functions must have a such
    instance as a first positional-only argument.
"""

from typing import Callable, List, Any, Optional, TypeVar
from functools import wraps
from typing import Any, Optional, Callable

T = TypeVar('T')

def _check_is_itemlike(f):

    @wraps(f)
    def g(*a, **k):

        a = list(a)
        assert len(a) > 0, f"must have at least one positional argument, got: ({a}, {k})"

        inst = a.pop(0)
        assert inst.__getattribute__("__getitem__"), f"{inst} must have `__getitem__` method"
        assert inst.__getattribute__("__setitem__"), f"{inst} must have `__setitem__` method"

        return f(inst, *a, **k)

    return g


try_get_first: Callable[[Any], Optional[Any]]
try_get_first = _check_is_itemlike(lambda l: l[0] if l else None)

try_pop_first: Callable[[List[T]], Optional[T]]
try_pop_first = lambda l: l[0] if l else None
