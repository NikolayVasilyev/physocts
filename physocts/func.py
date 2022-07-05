"""
file: func.py
author: Nikolay S. Vasil'ev
description: functional tools
"""

from typing import Callable, Any, TypeVar
from functools import partial, reduce

X = TypeVar("X")
Y = TypeVar("Y")


def apply_item(hlr: Callable[[X, Y], None], inst: X, itm: Y):
    """
    Apply handler `hlr` to an instance `inst` with item: `itm` and return `itm`;
    this is a convenient method to remove or apply some actions in lambda-style
    functions.
    """
    hlr(inst, itm)
    return itm


flip = Callable[[ Callable[[X, Y], Any] ], Callable[[Y, X], Any] ]
flip = lambda f: lambda x, y: f(y, x)


composite = Callable[..., Callable[[Any], Any]]
composite = lambda *fs: reduce( lambda g, f: lambda x: f(g(x)), fs[::-1], lambda x: x )
