#encoding: utf-8
import os
import sys
import glob
sys.path.append(os.path.join(os.path.dirname(__file__), "../parser"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../const"))

from parser.syntax import *
from const.token_type import *

lib_code = ""
libs = []

value_n = 0
indent = 0
in_expr = False
in_func = False
in_loop = False

def error():
    print("ERROR")
    sys.exit(-1)

def add_indent(code):
    if in_expr: return code[0]
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
    global in_expr

    name = tree.name
    t = tree.type
    
    in_expr = True
    expr = gen_python_code(tree.expr)
    in_expr = False

    if tree.expr is None:
        if t == "integer":
            expr = "_se_Integer(0)"
        elif t == "float":
            expr = "_se_Float(0.0)"

    return add_indent([f"_se_var_def(\"{name}\", {type_class[t]}, {expr})"])

def gen_assignment(tree):
    global in_expr
    name = tree.name
    expr = tree.expr

    in_expr = True
    expr = gen_python_code(expr)
    in_expr = False
    
    return add_indent([f"_se_assignment(\"{name}\", {expr})"])

def gen_func_def(tree):
    global in_func
    in_func = True

    name = tree.name
    args = tree.arg_names
    ret = tree.return_types

    code = add_indent([f"def {name}_():"])
    inc_indent()
    st = gen_python_code(tree.statements)
    if st == "": st = add_indent(["pass"])
    code += st
    dec_indent()

    arg_list = f"""[{", ".join(map(lambda x: "('" + x[0] + "', " + type_class[x[1]] + " )", args))}]"""
    code += add_indent([f"_se_functions[\"{name}\"] = [{name+'_'}, {arg_list}, [{', '.join(map(lambda x: type_class[x], ret))}]]"])

    in_func = False

    return code

def gen_return(tree):
    if not in_func:
        error()
    values = gen_python_code(tree.exprs)

    return add_indent([f"return [{values}]"])

def gen_call_func(tree):
    name = tree.name
    args = gen_python_code(tree.args)

    return add_indent([f"_se_call(\"{name}\", ({args}, ))"])

def gen_infinit_loop(tree):
    global in_loop 
    in_loop = True

    code = add_indent(["_se_assignment(\"#counter\", _se_Integer(1))"])
    code += add_indent(["while True:"])

    inc_indent()
    st = gen_python_code(tree.statements)
    code += st
    code += add_indent(["_se_assignment(\"#counter\", _se_add(_se_Ident(\"#counter\"), _se_Integer(1)))"])
    dec_indent()

    in_loop = False
    return code

def gen_count_loop(tree):
    global in_loop 
    in_loop = True

    code = add_indent(["_se_assignment(\"#counter\", _se_Integer(1))"])
    code += add_indent(["while True:"])

    inc_indent()
    st = gen_python_code(tree.statements)
    code += st
    n = gen_python_code(tree.n)
    code += add_indent(["_se_assignment(\"#counter\", _se_add(_se_Ident(\"#counter\"), _se_Integer(1)))"])
    #node.n < #count: break
    code += add_indent([f"if _se_lss({n}, _se_Ident(\"#counter\")):"])
    inc_indent()
    code += add_indent(["break"])
    dec_indent()
    dec_indent()

    in_loop = False
    return code

def gen_import(tree):
    global lib_code, libs

    prog_dir = os.path.dirname(__file__)

    names = tree.names

    for name in names:
        if name in libs: continue

        libs.append(name)

        if name == "PY":
            with open(prog_dir + "/libs/PY.py") as f:
                lib_code += f.read() + "\n"

    return ""

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

    return ", ".join(map(lambda x:f"({x})" ,arg_list))

def gen_expr(tree):
    global in_expr

    in_expr = True

    left = gen_python_code(tree.left)
    op = oper_f[tree.oper]
    right = gen_python_code(tree.right)

    vn = get_vn()

    in_expr = False
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

    IMPORT: gen_import,

    INFINIT_LOOP: gen_infinit_loop,
    COUNT_LOOP: gen_count_loop,

    EXPR: gen_expr,
    EXPRS: gen_exprs,
    ARGS: gen_args,
    INTEGER: gen_integer,
    FLOAT: gen_float,
    IDENT: gen_ident,
}

oper_f = {
    "+": "_se_add",
    "-": "_se_sub",
    "*": "_se_mul",
    "/": "_se_div",

    "==": "_se_equ", 
    "!=": "_se_neq", 
    "<": "_se_lss", 
    ">": "_se_gtr", 
    ">=": "_se_geq", 
    "<=": "_se_leq", 
}

type_class = {
    "integer": "_se_Integer",
    "float": "_se_Float",
    "bool": "_se_Bool",
}

def gen_python_code(tree):
    code = ""
    t = type(tree)
    if t in generator_f:
        code += generator_f[t](tree)

    return code

def gen_executable_code(tree):
    code = gen_python_code(tree)

    with open(os.path.dirname(__file__) + "/header.py", mode="r", encoding="utf-8") as f:
        header = f.read()

    with open(os.path.dirname(__file__) + "/runtime.py", mode="r", encoding="utf-8") as f:
        runtime_lib = f.read()

    return header + runtime_lib + lib_code + "#---\n\n" + code
