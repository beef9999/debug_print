"""
    Example:
    from debug_print import dprint
    dprint (obj, args, kwargs)
"""

from datetime import datetime
from inspect import currentframe, getframeinfo

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def frame_info_str():
    frameinfo = getframeinfo(currentframe())
    file_name = frameinfo.filename.split('/')[-1]
    return '{0}:{1} >>>'.format(file_name, frameinfo.lineno)

def dprint(*args):
    _dprint_options(getframeinfo(currentframe()).function, args)

def dprint_ok(*args):
    _dprint_options(getframeinfo(currentframe()).function, args)

def dprint_fail(*args):
    _dprint_options(getframeinfo(currentframe()).function, args)

def dprint_warning(*args):
    _dprint_options(getframeinfo(currentframe()).function, args)

def current_time_str():
    return '[%s]:' % datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def _dprint_options(func_name, args):
    if 'ok' in func_name:
        color_scheme_beginning = Color.OKGREEN
    elif 'fail' in func_name:
        color_scheme_beginning = Color.FAIL
    elif 'warning' in func_name:
        color_scheme_beginning = Color.WARNING
    else:
        color_scheme_beginning = Color.HEADER
    color_scheme_end = Color.ENDC
    ret_str = ''
    for i in args:
        if isinstance(i, dict):
            for j in i:
                ret_str += '{0}:{1}, '.format(repr(j), repr(i[j]))
        elif isinstance(i, list):
            for j in i:
                ret_str += repr(j) + ', '
        else:
            ret_str += repr(i) + ', '
    print ret_str
    print color_scheme_beginning, frame_info_str(), ret_str, color_scheme_end
