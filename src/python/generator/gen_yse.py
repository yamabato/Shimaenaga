#encoding: utf-8
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../parser"))

from parser.syntax import *

code = ""


def add_code(operator, *params):
    global code
    code += operator + " " + " ".join(map(str, params)) + "\n"

def gen_compound_statement(tree):
    code = ""
    for st in tree.statements:
        generator(st)

    return code

def gen_assignment(tree):
    name = tree.name
    expr = tree.expr

    generator(expr)
    add_code("pop", 0, "a")
    add_code("stv", name, "$a")

    return code
    
def gen_expr(tree):
    generator(tree.left)
    generator(tree.right)

    add_code("pop", 0, "b")
    add_code("pop", 0, "a")
    
    op = opers[tree.oper]
    add_code(op, "$a", "$b", "a")
    add_code("psh", 0, "$a")

    return ""

def gen_integer(tree):
    value = tree.value

    add_code("psh", 0, value)

def gen_ident(tree):
    name = tree.name

    add_code("psh", 0, name)

opers = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "div",
    "**": "pow",
    "%": "mod",
}

postfix_opers = {
    "++": "add",
    "--": "sub",
}

generators = {
    COMPOUND_STATEMENT: gen_compound_statement,
    ASSIGNMENT: gen_assignment,
    
    EXPR: gen_expr,

    INTEGER: gen_integer,
    IDENT: gen_ident,
}

def generator(tree):
    t = type(tree)
    if t in generators:
        generators[t](tree)
    else:
        print("ERROR")
        print(t)
        #sys.exit(-1)

    return code

