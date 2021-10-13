#encoding: utf-8
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../parser"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../const"))

from parser.syntax import *
from const.token_type import *

value_n = 0
indent = 0

def add_indent(code):
    return "\n".join(map(lambda x: " "*indent*4 + x, code)) + "\n"

def inc_indent():
    global indent

    indent += 1

def dec_indent():
    global indent

    indent -= 1

def get_vn():
    global value_n
    value_n += 1
    
    return value_n - 1

def gen_compound_statement(tree):
    code = ""
    for st in tree.statements:
        code += gen_python_code(st)

    return code

def gen_var_def(tree):
    name = tree.name
    t = tree.type
    expr = gen_python_code(tree.expr)

    if tree.expr is None:
        if t == "integer":
            expr = "_se_Integer(0)"
        elif t == "float":
            expr = "_se_Float(0.0)"

    return add_indent([f"_se_var_def(\"{name}\", {type_class[t]}, {expr})"])

def gen_assignment(tree):
    name = tree.name
    expr = tree.expr

    expr = gen_python_code(expr)
    
    return add_indent([f"_se_assignment(\"{name}\", {expr})"])

def gen_func_def(tree):
    name = tree.name
    args = tree.arg_names
    ret = tree.return_types

    code = add_indent([f"def {name}_({', '.join(map(lambda x: x[0], args))}):"])
    inc_indent()
    st = gen_python_code(tree.statements)
    if st == "": st = add_indent(["pass"])
    code += st
    dec_indent()

    code += add_indent([f"_se_functions[\"{name}\"] = [{name+'_'}, [{', '.join(map(lambda x:type_class[x[1]], args))}], [{', '.join(map(lambda x: type_class[x], ret))}]]"])

    return code

def gen_return(tree):
    values = gen_python_code(tree.exprs)

    return add_indent([f"return {values}"])

def gen_call_func(tree):
    name = tree.name
    args = gen_python_code(tree.args)

    return add_indent([f"_se_call(\"{name}\", ({args}))"])

def gen_infinit_loop(tree):
    code = add_indent(["_se_assignment(\"#counter\", _se_Integer(1))"])
    code += add_indent(["while True:"])

    inc_indent()
    st = gen_python_code(tree.statements)
    code += st
    code += add_indent(["_se_assignment(\"#counter\", _se_add(_se_Ident(\"#counter\"), _se_Integer(1)))"])
    dec_indent()

    return code

#---

def gen_exprs(tree):
    exprs = tree.exprs
    expr_list = []

    for expr in exprs:
        expr_list.append(gen_python_code(expr))

    return ", ".join(expr_list)

def gen_args(tree):
    args = tree.args
    arg_list = []

    for arg in args:
        arg_list.append(gen_python_code(arg))

    return ", ".join(arg_list)

def gen_expr(tree):
    left = gen_python_code(tree.left)
    op = oper_f[tree.oper]
    right = gen_python_code(tree.right)

    vn = get_vn()

    return f"{op}({left}, {right})"

def gen_integer(tree):
    value = tree.value
    return f"_se_Integer({value})"

def gen_float(tree):
    value = tree.value
    return f"_se_Float({value})"

def gen_ident(tree):
    name = tree.name
    return f"_se_Ident(\"{name}\")"

generator_f = {
    COMPOUND_STATEMENT: gen_compound_statement,

    VAR_DEF: gen_var_def,
    ASSIGNMENT: gen_assignment,

    CALL_FUNC: gen_call_func,
    FUNC_DEF: gen_func_def,
    RETURN: gen_return,

    INFINIT_LOOP: gen_infinit_loop,

    EXPR: gen_expr,
    EXPRS: gen_exprs,
    ARGS: gen_args,
    INTEGER: gen_integer,
    FLOAT: gen_float,
    IDENT: gen_ident,
}

oper_f = {
    "+": "_se_add",
    "*": "_se_mul",
}

type_class = {
    "integer": "_se_Integer",
    "float": "_se_Float",
}

def gen_python_code(tree):
    code = ""
    t = type(tree)
    if t in generator_f:
        code += generator_f[t](tree)

    return code

def gen_executable_code(tree):
    code = gen_python_code(tree)

    with open(os.path.dirname(__file__) + "/runtime.py", mode="r", encoding="utf-8") as f:
        runtime_lib = f.read()

    return runtime_lib + code
