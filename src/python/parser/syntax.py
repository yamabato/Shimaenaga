#encoding: utf-8

class COMPOUND_STATEMENT:
    def __init__(self):
        self.statements = []
        self.n = 0

    #expr: EXPR
    def add_statement(self, statement):
        self.statements.append(statement)

    def next(self):
        self.n += 1
        

class STATEMENT:
    #statement
    def __init__(self, statement):
        self.statement = None

#variable definition
class VAR_DEF:
    def __init__(self, name=None, var_type=None, expr=None):
        self.name = None
        self.type = None
        self.expr = None

class ASSIGNMENT:
    def __init__(self, name=None, expr=None):
        self.name = name
        self.expr = expr

class COUNT_LOOP:
    def __init__(self, n=None, statements=None):
        self.n = n
        self.statements = statements

class INFINIT_LOOP:
    def __init__(self, statements=None):
        self.statements = statements

class BREAK:
    def __init__(self):
        pass

class CONTINUE:
    def __init__(self):
        pass

#conditional branch
class BRANCH:
    def __init__(self, if_clause=None, elif_clauses=None, else_clause=None):
        self.if_clause = if_clause
        self.elif_clauses = elif_clauses
        self.else_clause = else_clause

class IF:
    def __init__(self, condition=None, statements=None):
        self.condition = condition
        self.statements = statements

class ELIF_CLAUSES:
    def __init__(self, elif_clauses=[]):
        self.elif_clauses = elif_clauses

    def add_clause(self, elif_clause):
        self.elif_clauses.append(elif_clause)

class ELIF:
    def __init__(self, condition=None, statements=None):
        self.condition = condition
        self.statements = statements

class ELSE:
    def __init__(self, statements=None):
        self.statements = statements

class SWITCH_CONDITION:
    def __init__(self, case_clauses=None, else_clause=None, finally_clause=None):
        self.case_clauses = case_clauses
        self.else_clause = else_clause
        self.finally_clause = finally_clause

class SWITCH_VALUE:
    def __init__(self, value=None, case_clauses=None, else_clause=None, finally_clause=None):
        self.value = value
        self.case_clauses = case_clauses
        self.else_clause = else_clause
        self.finally_clause = finally_clause

#case clause
class MATCH_CONDITION:
    def __init__(self, condition=None, statements=None):
        self.condition = condition
        self.statements = statements

class MATCH_VALUE:
    def __init__(self, exprs=None, statements=None):
        self.exprs = exprs
        self.statements = statements

class MATCH_CONDITION_CLAUSES:
    def __init__(self, match_condition_clauses=[]):
        self.match_condition_clauses = match_condition_clauses

    def add_match_condition_clause(self, clause):
        self.match_condition_clauses.append(clause)

class MATCH_VALUE_CLAUSES:
    def __init__(self, match_value_clauses=[]):
        self.match_value_clauses = match_value_clauses

    def add_match_value_clause(self, clause):
        self.match_value_clauses.append(clause)

class FINALLY:
    def __init__(self, statements=None):
        self.statements = statements

class FUNC_DEF:
    pass

class ARGS:
    def __init__(self, args=[]):
        self.args = args

    def add_arg(self, arg):
        self.args.append(arg)

class RETURN:
    def __init__(self, exprs=None):
        self.exprs = exprs

class EXPRS:
    def __init__(self, exprs=[]):
        self.exprs = exprs

    def add_expr(self, expr):
        self.exprs.append(expr)

class IMPORT:
    def __init__(self, names=[]):
        self.names = []

    def add_name(self, name):
        self.names.append(name)

class CALL_LIB_FUNC:
    def __init__(self, name=None, lib=None, args=None):
        self.name = name
        self.lib = lib
        self.args = args

class CALL_FUNC:
    def __init__(self, name=None, args=None):
        self.name = name
        self.args = args

#postfix operators, suck as ++ or --
class POSTFIX:
    def __init__(self, name=None, oper=None):
        self.name = name
        self.oper = oper

class EXPR:
    def __init__(self, left=None, oper=None, right=None):
        self.left = left
        self.right = right
        self.oper = oper

class INTEGER:
    def __init__(self, value):
        self.value = value

class FLOAT:
    def __init__(self, value):
        self.value = value

class IDENT:
    def __init__(self, name):
        self.name = name

class STRING:
    def __init__(self, value):
        self.value = value

class BOOL:
    def __init__(self, value):
        self.value = value

class LIST:
    pass

class MAP:
    pass

