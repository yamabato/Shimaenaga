#encoding: utf-8
from .syntax import *

indent = 0

def increase_indent():
    global indent
    indent += 2

def decrease_indent():
    global indent
    indent -= 2

def write(arg):
    print(" "*indent + str(arg))

def compound_statement_print(node):
    for st in node.statements:
        pretty_print(st)

def expr_print(node):
    write(":EXPR")
    increase_indent()

    pretty_print(node.left)
    write(node.oper)
    pretty_print(node.right)

    decrease_indent()

def integer_print(node):
    write(":INTEGER")
    increase_indent()

    write(node.value)

    decrease_indent()

def var_def_print(node):
    name = node.name
    var_type = node.type
    expr = node.expr
    

    write(":VAR_DEF")
    increase_indent()

    write(name)
    write(var_type)
    pretty_print(expr)

    decrease_indent()

def assignment_print(node):
    name = node.name
    expr = node.expr
   
    write(":ASSIGNMENT")
    increase_indent()

    write(name)
    pretty_print(expr)

    decrease_indent()

def infinit_loop_print(node):
    write(":INFINIT_LOOP")
    increase_indent()

    pretty_print(node.statements)

    decrease_indent()

def count_loop_print(node):
    write(":COUNT_LOOP")
    increase_indent()

    pretty_print(node.n)
    pretty_print(node.statements)

    decrease_indent()
    

syntax_f = {
    COMPOUND_STATEMENT: compound_statement_print,

    EXPR: expr_print,
    INTEGER: integer_print,
    VAR_DEF: var_def_print,
    ASSIGNMENT: assignment_print,
    INFINIT_LOOP: infinit_loop_print,
    COUNT_LOOP: count_loop_print,
}

def pretty_print(node):
    node_type = type(node)

    if node_type in syntax_f:
        print_f = syntax_f[node_type]
        print_f(node)
    else:
        pass


    
