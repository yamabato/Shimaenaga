#encoding: utf-8
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../parser"))

from parser.syntax import *

value_n = 0

def get_vn():
    global value_n
    value_n += 1
    
    return value_n - 1

def gen_compound_statement(tree):
    code = ""
    for st in tree.statements:
        code += gen_python_code(st)

    return code

def gen_assignment(tree):
    global code
    name = tree.name
    expr = tree.expr

    expr = gen_expr(expr)
    
    return f"{name} = {expr}\n"

def gen_expr(tree):
    left = gen_python_code(tree.left)
    op = tree.oper
    right = gen_python_code(tree.right)

    vn = get_vn()

    return f"({left} {op} {right})"

def gen_integer(tree):
    value = tree.value
    return f"_integer({value})"

def gen_ident(tree):
    name = tree.name
    return f"_ident(\"{name}\")"

generator_f = {
    COMPOUND_STATEMENT: gen_compound_statement,

    ASSIGNMENT: gen_assignment,

    EXPR: gen_expr,
    INTEGER: gen_integer,
    IDENT: gen_ident,
}

def gen_python_code(tree):
    code = ""
    t = type(tree)
    if t in generator_f:
        code += generator_f[t](tree)

    return code
