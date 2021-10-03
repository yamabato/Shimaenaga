#encoding: utf-8
from .syntax import *

indent = 0

def increase_indent():
    global indent
    indent += 4

def decrease_indent():
    global indent
    indent -= 4

def write(arg):
    print(" "*indent + str(arg))

def compound_statement_print(node):
    write(":STATEMENTS")
    increase_indent()

    for st in node.statements:
        pretty_print(st)

    decrease_indent()

def expr_print(node):
    write(":EXPR")
    increase_indent()

    pretty_print(node.left)
    write(node.oper)
    pretty_print(node.right)

    decrease_indent()

def postfix_print(node):
    write(":POSTFIX")
    increase_indent()

    write(node.name)
    write(node.oper)

    decrease_indent()

def integer_print(node):
    write(":INTEGER")
    increase_indent()

    write(node.value)

    decrease_indent()

def float_print(node):
    write(":FLOAT")
    increase_indent()

    write(node.value)

    decrease_indent()

def ident_print(node):
    write(":IDENT")
    increase_indent()

    write(node.name)

    decrease_indent()

def string_print(node):
    write(":STRING")
    increase_indent()

    write(node.value)

    decrease_indent()

def bool_print(node):
    write(":BOOL")
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

def break_print(node):
    write(":BREAK")

def continue_print(node):
    write(":CONTINUE")

def branch_print(node):
    write(":BRANCH")
    increase_indent()

    pretty_print(node.if_clause)

    if node.elif_clauses is not None:
        pretty_print(node.elif_clauses)

    if node.else_clause is not None:
        pretty_print(node.else_clause)

    decrease_indent()

def if_print(node):
    write(":IF")
    increase_indent()

    pretty_print(node.condition)
    pretty_print(node.statements)

    decrease_indent()

def elif_print(node):
    write(":ELIF")
    increase_indent()

    pretty_print(node.condition)
    pretty_print(node.statements)

    decrease_indent()


def elif_clauses_print(node):
    for clause in node.elif_clauses:
        pretty_print(clause)

def else_print(node):
    write(":ELSE")
    increase_indent()

    pretty_print(node.statements)

    decrease_indent()

def switch_condition_print(node):
    write(":SWITCH_CONDITION")
    increase_indent()

    pretty_print(node.case_clauses)

    if node.else_clause is not None:
        pretty_print(node.else_clause)

    if node.finally_clause is not None:
        pretty_print(node.finally_clause)

    decrease_indent()

def switch_value_print(node):
    write(":SWITCH_VALUE")
    increase_indent()

    pretty_print(node.case_clauses)

    if node.else_clause is not None:
        pretty_print(node.else_clause)

    if node.finally_clause is not None:
        pretty_print(node.finally_clause)

    decrease_indent()

def match_condition_clauses_print(node):
    write(":MATCH_CONDITION_CLAUSES")
    increase_indent()

    for match in node.match_condition_clauses:
        pretty_print(match)

    decrease_indent()

def match_condition_print(node):
    write(":MATCH_CONDITION")
    increase_indent()

    pretty_print(node.condition)
    pretty_print(node.statements)

    decrease_indent()

def match_value_clauses_print(node):
    write(":MATCH_VALUE_CLAUSES")
    increase_indent()

    for match in node.match_value_clauses:
        pretty_print(match)

    decrease_indent()

def match_value_print(node):
    write(":MATCH_VALUE")
    increase_indent()

    pretty_print(node.exprs)
    pretty_print(node.statements)

    decrease_indent()

def finally_print(node):
    write(":FINALLY")
    increase_indent()

    pretty_print(node.statements)

    decrease_indent()


def return_print(node):
    write(":RETURN")
    increase_indent()
    
    if node.exprs is not None:
        pretty_print(node.exprs)

    decrease_indent()

def exprs_print(node):
    write(":EXPRS")
    increase_indent()

    for expr in node.exprs:
        pretty_print(expr)

    decrease_indent()

def import_print(node):
    write(":IMPORT")
    increase_indent()

    for name in node.names:
        write(name)

    decrease_indent()

def call_func_print(node):
    write(":CALL_FUNC")
    increase_indent()

    write(node.name)

    if node.args is not None:
        pretty_print(node.args)

    decrease_indent()

def call_lib_func_print(node):
    write(":CALL_LIB_FUNC")
    increase_indent()

    write(node.name)
    write(node.lib)

    if node.args is not None:
        pretty_print(node.args)

    decrease_indent()

def args_print(node):
    write(":ARGS")
    increase_indent()

    for arg in node.args:
        pretty_print(arg)

    decrease_indent()

syntax_f = {
    COMPOUND_STATEMENT: compound_statement_print,

    EXPR: expr_print,
    POSTFIX: postfix_print,
    INTEGER: integer_print,
    FLOAT: float_print,
    IDENT: ident_print,
    STRING: string_print,
    BOOL: bool_print,

    VAR_DEF: var_def_print,
    ASSIGNMENT: assignment_print,

    INFINIT_LOOP: infinit_loop_print,
    COUNT_LOOP: count_loop_print,
    BREAK: break_print,
    CONTINUE: continue_print,
    
    BRANCH: branch_print,
    IF: if_print,
    ELIF: elif_print,
    ELIF_CLAUSES: elif_clauses_print,
    ELSE: else_print,

    SWITCH_CONDITION: switch_condition_print,
    SWITCH_VALUE: switch_value_print,
    MATCH_CONDITION_CLAUSES: match_condition_clauses_print,
    MATCH_CONDITION: match_condition_print,
    MATCH_VALUE_CLAUSES: match_value_clauses_print,
    MATCH_VALUE: match_value_print,
    FINALLY: finally_print,

    RETURN: return_print,
    EXPRS: exprs_print,

    IMPORT: import_print,

    CALL_FUNC: call_func_print,
    CALL_LIB_FUNC: call_lib_func_print,
    ARGS: args_print,
}

def pretty_print(node):
    node_type = type(node)

    if node_type in syntax_f:
        print_f = syntax_f[node_type]
        print_f(node)
    else:
        pass


    
