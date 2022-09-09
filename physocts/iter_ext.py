"""
file: iter_ext.py
author: Nikolay S. Vasil'ev
description: additional tools for iterators
"""
from typing import List, Dict, Tuple, Any, Set, Optional, Callable, FrozenSet, Iterable, TypeVar

from functools import partial
from more_itertools import take

from .func import bind_maybes


T = TypeVar("T")


maybe_head: Callable[ [Iterable[T]], Optional[T] ]
maybe_head = bind_maybes(
    lambda x: x[0] if x else None,
    partial(take, 1))


def test_maybe_head():
    """tests"""
    assert maybe_head(iter([1,2,3])) == 1
    assert maybe_head(iter([])) is None
    assert maybe_head([1,2,3]) == 1
    assert maybe_head([]) is None
    assert maybe_head({1,2,3}) in [1, 2, 3]
    assert maybe_head(set()) is None
