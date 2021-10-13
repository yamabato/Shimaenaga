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

def gen_call_func(tree):
    name = tree
    args = gen_python_code(tree.args)

    return add_indent([f"{name}({args})"])

def gen_exprs(tree):
    exprs = tree.exprs
    expr_list = []

    for expr in exprs:
        expr_list.append(gen_python_code(expr))

    return ", ".join(expr_list)

def gen_expr(tree):
    left = gen_python_code(tree.left)
    op = oper_f[tree.oper]
    right = gen_python_code(tree.right)

    vn = get_vn()

    return f"{op}({left}, {right})"

def gen_integer(tree):
    value = tree.value
    return f"_se_Integer({value})"

def gen_ident(tree):
    name = tree.name
    return f"_se_Ident(\"{name}\")"

generator_f = {
    COMPOUND_STATEMENT: gen_compound_statement,

    VAR_DEF: gen_var_def,
    ASSIGNMENT: gen_assignment,

    CALL_FUNC: gen_call_func,

    EXPR: gen_expr,
    INTEGER: gen_integer,
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
