"""
file: jsonlike.py
author: Nikolay S. Vasil'ev
description: handle JSON structures
"""

import json
from typing import Callable, Tuple, Union, Optional
from functools import partial
from pathlib import Path

from physocts.wrappers import wrap_in_either

from .log import force_stderr_log
from .either import Either, EitherType
from .exceptions import report_traceback

FileNameType = Union[str, Path]


def try_loads(s: str) -> Optional[dict]:
    """
    try to load a string with JSON, return a dictionary on success and None
    otherwise
    """
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None

def unsafe_write(data: dict, flnm: FileNameType, **k):
    with open(flnm, 'w', encoding="utf-8") as fid:
        json.dump(data, fid, **k)

write = wrap_in_either(unsafe_write)


def unsafe_load(flnm: FileNameType, **k) -> dict:
    with open(flnm, 'r', encoding="utf-8") as fid:
        return json.load(fid, **k)

load = wrap_in_either(unsafe_load)


flat: Callable[[dict], EitherType[str]]
flat = wrap_in_either(json.dumps)


pretty: Callable[[dict], EitherType[str]]
pretty = wrap_in_either(partial(json.dumps, indent=" "*4))


def info(data: dict):
    with force_stderr_log(1) as l:
        if not (res := pretty(data)):
            l.error("Failed to dump to JSON string:\n%r", res.value)
            return

        l.info("JSON=\n" + res.value)
