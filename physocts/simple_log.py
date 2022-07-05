"""
file: simple_log.py
author: Nikolay S. Vasil'ev
description: a simple logger implementation; this is used when a usual logger
    is not rational or may not applied
"""
import sys

from functools import partial
from typing import Callable
from contextlib import contextmanager

# pylint: disable=W0603

SLOG = False
SLOG_DEBUG = False
SLOG_INFO = False


def _simple_log(relax_checker: Callable[[], bool], tag: str, clr: int, msg: str, /, *a):

    if relax_checker():
        return

    assert isinstance(clr, int)

    print(\
        f"\033[1;40;{clr}m[{tag}] \033[m\033[0;40;{clr}m" + \
            f"{sys.argv[0] or r'>>>'}: " + msg % a + "\033[m",
        file=sys.stderr)


def enable_simple_log():
    global SLOG
    SLOG = True

def enable_simple_log_debug():
    global SLOG_DEBUG
    SLOG_DEBUG = True

def enable_simple_log_info():
    global SLOG_INFO
    SLOG_INFO = True

def disable_simple_log():
    global SLOG
    SLOG = True

def disable_simple_log_debug():
    global SLOG_DEBUG
    SLOG_DEBUG = True

def disable_simple_log_info():
    global SLOG_INFO
    SLOG_INFO = True


ERROR_CLR = 31
WARNING_CLR = 33
INFO_CLR = 35
DEBUG_CLR = 36


@contextmanager
def enabled(b_debug: bool=False):
    global SLOG, SLOG_INFO, SLOG_DEBUG

    (old_slog, old_slog_info, old_slog_debug) = (SLOG, SLOG_INFO, SLOG_DEBUG)
    SLOG = True
    SLOG_INFO = True
    SLOG_DEBUG = b_debug or old_slog_debug

    yield

    (SLOG, SLOG_INFO, SLOG_DEBUG) = (old_slog, old_slog_info, old_slog_debug)


debug = partial(_simple_log, lambda: not (SLOG and SLOG_DEBUG), "DEBUG", DEBUG_CLR)
info = partial(_simple_log, lambda: not (SLOG and (SLOG_DEBUG or SLOG_INFO)), "INFO", INFO_CLR)
warning = partial(_simple_log, lambda: not SLOG, "WARNING", WARNING_CLR)
error = partial(_simple_log, lambda: not SLOG, "ERROR", ERROR_CLR)
