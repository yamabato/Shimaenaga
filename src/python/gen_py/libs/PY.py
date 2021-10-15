def _se_PY_putchar():
    n = _se_get_value(_se_Ident("n"))
    print(chr(n), end="")
    sys.stdout.flush()

_se_functions["_se_PY_putchar"] = [_se_PY_putchar, [("n", _se_Integer)], []]
