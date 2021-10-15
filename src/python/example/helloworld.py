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
        return _se_environment[value.name][1]
        return _se_get_value(_se_environment[value.name][1])

def _se_is_num(value):
    if isinstance(value, _se_Integer) or isinstance(value, _se_Float):
        return True
    
    if isinstance(value, _se_Ident) and _se_is_num(_se_environment[value.name][1]):
        return True

    return False

def _se_add(v1, v2):
    if _se_is_num(v1):
        if _se_is_num(v2):
            return _se_Integer(_se_get_value(v1) + _se_get_value(v2))
        _se_error()

def _se_mul(v1, v2):
    if _se_is_num(v1):
        if _se_is_num(v2):
            return _se_Integer(_se_get_value(v1) * _se_get_value(v2))
        _se_error()

def _se_var_def(name, t, value):
    if name in _se_environment: _se_error()

    _se_environment[name] = [t, value]

def _se_assignment(name, value):
    if name not in _se_environment: _se_error()

    t = _se_environment[name][0]
    if not isinstance(value, t): _se_error()

    _se_environment[name][1] = value

def _se_call(name, args):
    global _se_environment
    if name not in _se_functions: _se_error()

    f, arg_types, ret = _se_functions[name]

    if len(arg_types) != len(args): _se_error()

    args_ = []
    for arg in args:
        if isinstance(arg, _se_Ident):
            args_.append(_se_get_value(arg))
        else:
            args_.append(arg)
    
    for arg, at in zip(args_, arg_types):
        if not isinstance(arg, at[1]): _se_error()

    env = _se_environment.copy()

    for at, arg in zip(arg_types, args_):
        if at[0] not in _se_environment:
            _se_var_def(*at, arg)
        else:
            _se_assignment(at[0], arg)

    ret_value = f(*map(lambda x: _se_get_value(x), args))

    if (0 if ret_value is None else len(ret_value)) != len(ret): _se_error()

    if ret_value is not None:
        for r, rt in zip(ret_value, ret):
            if not isinstance(r, rt): _se_error()

        if len(ret_value) == 1:
            ret_value = ret_value[0]

    _se_environment = env

    return ret_value

#---

#name: [type, value]
_se_environment = {}

#name: [func, args, ret]
_se_functions = {}

_se_var_def("#counter", _se_Integer, _se_Integer(0))

#---

def _se_PY_putchar(n):
    if isinstance(n, _se_Integer):
        print(chr(_se_get_value(n)), end="")

_se_functions["_se_PY_putchar"] = [_se_PY_putchar, [("n", _se_Integer)], []]

#---

def put_(n):
    _se_call("_se_PY_putchar", ((_se_Ident("n")), ))
_se_functions["put"] = [put_, [('n', _se_Integer )], []]
_se_call("put", ((_se_Integer(72)), ))
_se_call("put", ((_se_Integer(101)), ))
_se_call("put", ((_se_Integer(108)), ))
_se_call("put", ((_se_Integer(108)), ))
_se_call("put", ((_se_Integer(111)), ))
_se_call("put", ((_se_Integer(44)), ))
_se_call("put", ((_se_Integer(32)), ))
_se_call("put", ((_se_Integer(87)), ))
_se_call("put", ((_se_Integer(111)), ))
_se_call("put", ((_se_Integer(114)), ))
_se_call("put", ((_se_Integer(108)), ))
_se_call("put", ((_se_Integer(100)), ))
_se_call("put", ((_se_Integer(33)), ))
_se_call("put", ((_se_Integer(33)), ))
_se_call("put", ((_se_Integer(10)), ))
