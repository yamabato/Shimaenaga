#encoding: utf-8
import sys

class _se_Integer:
    def __init__(self, value):
        self.value = value

class _se_Float:
    def __init__(self, value):
        self.value = value

class _se_Ident:
    def __init__(self, name):
        self.name = name

#---

def _se_error():
    print("ERROR")
    sys.exit(-1)

def _se_get_value(value):
    if isinstance(value, _se_Integer):
        return value.value

    if isinstance(value, _se_Float):
        return value.value

    if isinstance(value, _se_Ident):
        return _se_get_value(_se_environment[value.name][1])

def _se_is_num(value):
    if isinstance(value, _se_Integer) or isinstance(value, _se_Float):
        return True
    return False

def _se_add(v1, v2):
    if _se_is_num(v1):
        if _se_is_num(v2):
            return _se_Integer(v1.value + v2.value)
        _se_error()

def _se_mul(v1, v2):
    if _se_is_num(v1):
        if _se_is_num(v2):
            return _se_Integer(v1.value * v2.value)
        _se_error()

def _se_var_def(name, t, value):
    if name in _se_environment: _se_error()

    _se_environment[name] = [t, value]

def _se_assignment(name, value):
    if name not in _se_environment: _se_error()

    t = _se_environment[name][0]
    if not isinstance(value, t): _se_error()

    _se_environment[name][1] = value

def _se_print(*values):
    for v in values:
        print(_se_get_value(v), end=" ")

#---

#name: [type, value]
_se_environment = {}
