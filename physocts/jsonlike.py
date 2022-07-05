"""
file: jsonlike.py
author: Nikolay S. Vasil'ev
description: handle JSON structures
"""

import json
from typing import Callable, Tuple
from functools import partial

from .log import force_stderr_log
from .either import Either, EitherType
from .exceptions import report_traceback

def write(data: dict, flnm: str="tmp.json") -> EitherType[Tuple[()]]:
    try:
        with open(flnm, 'w', encoding="utf-8") as fid:
            json.dump(data, fid)

    except:  # pylint: disable=W0702
        return Either.left(report_traceback())

    return Either.right(())


def load(flnm: str) -> dict:
    with open(flnm, 'r', encoding="utf-8") as fid:
        return json.load(fid)

flat: Callable[[dict], str]
flat = json.dumps

pretty: Callable[[dict], str]
pretty = partial(json.dumps, indent=" "*4)

def info(data: dict):
    with force_stderr_log(1) as l:
        l.info("JSON=\n" + pretty(data))
