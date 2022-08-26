"""
file: string_ext.py
author: Nikolay S. Vasil'ev
description: common tools to handle with strings
"""

from typing import List, Dict, Tuple, Any, Set, Optional, Callable, FrozenSet, Iterable
from functools import partial
from .func import flip, bind_maybes

to_readable_text: Callable[ [Optional[str]], Optional[str] ]
to_readable_text = bind_maybes(partial(flip(str.translate), {i: "" for i in range(32)}))
