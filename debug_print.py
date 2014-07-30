"""
    Example:
    from debug_print import dprint
    dprint(obj, args, kwargs)
"""

from datetime import datetime
from inspect import currentframe, getframeinfo
import os
import sys


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

def findCaller():
    f = currentframe()
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", 0, "(unknown function)"
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        rv = (co.co_filename, f.f_lineno, co.co_name)
        break
    return rv



def frame_info_str(args):
    #frameinfo = getframeinfo(currentframe())
    fn, lno, func = findCaller()
    fn = fn.split('/')[-1]
    return '{0}:{1} >>>'.format(fn, lno)

def dprint(*args):
    _dprint_options(getframeinfo(currentframe()).function, args)

def dprint_ok(*args):
    _dprint_options(getframeinfo(currentframe()).function, args)

def dprint_fail(*args):
    _dprint_options(getframeinfo(currentframe()).function, args)

def dprint_warning(*args):
    _dprint_options(getframeinfo(currentframe()).function, args)

def current_time_str():
    return '[%s]' % datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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
            ret_str += '{ '
            for j in i:
                ret_str += '{0}:{1}, '.format(repr(j), repr(i[j]))
            ret_str += '}, '
        elif isinstance(i, list):
            ret_str += '[ '
            for j in i:
                ret_str += repr(j) + ', '
            ret_str += '], '
        else:
            ret_str += repr(i) + ', '
    print color_scheme_beginning, current_time_str(), frame_info_str(args)
    print ret_str, color_scheme_end
