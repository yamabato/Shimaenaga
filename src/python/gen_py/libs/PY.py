def _se_PY_putchar(n):
    print(chr(_se_get_value(n)), end="")

_se_functions["_se_PY_putchar"] = [_se_PY_putchar, [("n", _se_Integer)], []]
