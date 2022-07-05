"""
Parsec logging

Logging setup example.
The following commands enable syslog and log file for errors and higher
and stdout for info and higher:

>>> enable_syslog()
>>> enable_rotating_file()
>>> enable_stdout(logging.INFO)
>>> log.setLevel(logging.INFO)

"""
import os
import sys
from functools import partial
from logging import getLogger, Logger, Filterer, Formatter, Handler
from logging import WARNING
from logging import handlers, StreamHandler
from datetime import datetime as dt
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Dict, List, Callable, Union

from physocts.func import apply_item

DEFAULT_LOGGER_LEVEL = 30
DEFAULT_LOG_FILE_NAME = "log.log"
DEFAULT_LOGGER_NAME = "soners"
ROTATING_FILE_MAX_SIZE_MB = 1
BACKUP_COUNT = 5

def get_logger() -> Logger:
    """Returns a default logger"""
    return getLogger(DEFAULT_LOGGER_NAME)


def clear_logger(l: Optional[Logger] = None) -> dict:
    """
    Removes all handlers and filters from the logger;
    returns a dictionary with removed items.
    """
    l = l or get_logger()

    return {"handlers": [apply_item(Logger.removeHandler, l, h) for h in list(l.handlers)],
            "filters": [apply_item(Filterer.removeFilter, l, f) for f in list(l.filters)]}


#
#   Formatters
#
class FileLogFormatter(Formatter):
    """A logger for a rotating file log"""
    def __init__(self):
        super().__init__(fmt="[%(levelname)s] - %(asctime)s " + \
                             "PRC_%(process)d(THD=%(threadName)s) " + \
                             "%(module)s.%(funcName)s(LNO=%(lineno)d): \n" + \
                             "\t%(message)s\n---")

class ColoredLogFormatter(Formatter):
    """A colorful logger with a beauty console output and useful trace data, enjoy!

    Works in Linux consoles only.
    Fore more info on console colors and formatting:
        `https://misc.flogisoft.com/bash/tip_colors_and_formatting`
    """
    def __init__(self, datefmt=None):

        self.main_pid = os.getpid()

        super().__init__(fmt="%(message)s", datefmt=datefmt)

    def format(self, record):
        fmt = type("TextFormat", (object, ), {
            "normal": "{:s}",
            "caption": type("TextFormatCaption", (object, ), {
                "debug": "\033[34;7;1m{: ^9.7s}\033[0m",
                "info": "\033[35;7;1m{: ^9.7s}\033[0m",
                "warning": "\033[33;7;1m{: ^9.7s}\033[0m",
                "error": "\033[31;7;1m{: ^9.7s}\033[0m",
                "critical": "\033[31;7;1m{: ^9.7s}\033[0m",
                "log": "\033[37;7;1m{: ^10.8s}\033[0m"}),
            "trace_info": "\033[37;3;2m{:s}\033[0m",
            "process": "\033[43;100;1m PID:{:s} \033[0m",
            "thread": "\033[43;100;1m Thread:{:s} \033[0m"})

        message = fmt.normal.format(record.getMessage())
        thread_name = record.threadName
        if thread_name != "MainThread":
            thread = fmt.thread.format(thread_name)
            # indent = fmt.thread.format(" "*len(thread_name))
        else:
            thread = ""

        indent = ""

        if self.main_pid != record.process:
            process = fmt.process.format(str(record.process))
        else:
            process = ""

        cur_time = fmt.trace_info.format(dt.now().isoformat())

        path_name = record.pathname
        func_name = fmt.trace_info.format(record.funcName)
        line_no = fmt.trace_info.format(str(record.lineno))

        cur_format = getattr(fmt.caption, record.levelname.lower(), fmt.caption.log)
        level_name = cur_format.format(record.levelname)
        # level_no = record.levelno

        message = "\033[0m{:s}{:s} ".format(indent, cur_time) \
                  + "{:s}.{:s}:{:s}\n".format(path_name, func_name, line_no) \
                  + "{:s}{:s}{:s} {:s}".format(process, thread, level_name, message)

        return message

#
#   Handlers
#

class SysLogHandler(handlers.SysLogHandler):
    """Syslog handler"""
    def __init__(self):
        super().__init__(address="/dev/log")

#
#   Setup default logger
#

def setup_logger(level: int, logger: Logger, formatter: Formatter, handler: Handler):
    """
    Setup logger with custom formatter and Handler
    """
    level = level or WARNING
    assert 0 <= level <= 50

    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def enable_stdout(level: Optional[int]=None):
    """
    Enable logger with the output to stdout stream
    """
    formatter = ColoredLogFormatter()
    logger = getLogger(DEFAULT_LOGGER_NAME)
    setup_logger(level, logger, formatter, StreamHandler(sys.stdout))


def enable_stderr(level: Optional[int]=None):
    """
    Enable logger with the output to stderr stream
    """
    formatter = ColoredLogFormatter()
    logger = getLogger(DEFAULT_LOGGER_NAME)
    setup_logger(level, logger, formatter, StreamHandler(sys.stderr))


def _enable_file(
        level: int,
        path: Union[str, Path],
        file_log_handler: Callable[[ str ], None] ):

    logger = getLogger(DEFAULT_LOGGER_NAME)

    path = Path(path).absolute()
    if not path.parent.is_dir():
        raise NotADirectoryError("Log file parent directory %s does not exist" % path.parent)

    setup_logger(level,
                 logger,
                 FileLogFormatter(),
                 file_log_handler(path))

def enable_file(
        level: Optional[int]=None,
        path: Optional[Union[str, Path]]=None):
    """
    Enable file logging;
    NOTE:
        A watched file handler is used to work well with Unix `logrotate`
    """

    _enable_file(
        level=level or DEFAULT_LOGGER_LEVEL,
        path=path or Path("./").absolute()/Path(DEFAULT_LOG_FILE_NAME),
        file_log_handler=handlers.WatchedFileHandler)


def enable_rotating_file(
        level: Optional[int]=None,
        path: Optional[Union[str, Path]]=None,
        max_size: Optional[int]=ROTATING_FILE_MAX_SIZE_MB*1024*1024,
        backupCount: Optional[int]=BACKUP_COUNT):
    """
    Enable logger with the rotating file output;
    `max_size` is a maximum file size in Mb
    """

    _enable_file(
        level=level or DEFAULT_LOGGER_LEVEL,
        path=path or Path("./").absolute()/Path(DEFAULT_LOG_FILE_NAME),
        file_log_handler=partial(
            handlers.RotatingFileHandler,
            maxBytes=max_size,
            backupCount=backupCount))


def _with_forced_log(
        level: int,
        log_handler: Callable[[Optional[int]], None]):

    # save and clear the logger's state
    l = get_logger()
    d = clear_logger(l)

    log_handler(level)

    yield l

    # return previous logger state
    _ = clear_logger(l)
    _ = [ l.addFilter(fltr) for fltr in d["filters"] ]
    _ = [ l.addHandler(hlr) for hlr in d["handlers"] ]


@contextmanager
def with_forced_stderr_log(level: Optional[int]=None):
    yield from _with_forced_log(level or DEFAULT_LOGGER_LEVEL, enable_stderr)


@contextmanager
def with_forced_rfile_log(
        level: Optional[int]=None,
        path: str="./log.log"):
    yield from _with_forced_log(
        level or DEFAULT_LOGGER_LEVEL,
        partial(enable_rotating_file, path=path))


@contextmanager
def with_forced_file_log(
        level: Optional[int]=None,
        path: str="./log.log"):
    yield from _with_forced_log(
        level or DEFAULT_LOGGER_LEVEL,
        partial(enable_file, path=path))
