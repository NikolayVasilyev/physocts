"""
file: exceptions.py
author: Nikolay S. Vasil'ev
description: handle exceptions
"""

import sys

def report_traceback() -> str:

    info = sys.exc_info()

    if not (trb := info[2]):
        return "No errors"

    tr_msg = str()
    while (trb := getattr(trb, "tb_next", None)):
        tr_msg += \
            "---\n" \
            f"line: {trb.tb_lineno}\n" \
            f"file: {trb.tb_frame.f_code.co_filename}\n"  \
            f"module: {trb.tb_frame.f_code.co_name}\n"
    return tr_msg + \
        "===\n" \
        f"Error message: {type(info[1]).__name__}: {str(info[1])}"
