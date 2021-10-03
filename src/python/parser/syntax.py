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
    pass

class CONTINUE:
    pass

class IF:
    pass

#conditional branch
class BRANCH:
    pass

class IF:
    pass

class ELIF:
    pass

class ELSE:
    pass

class SWITCH:
    pass

#case clause
class MATCH:
    pass

class FINALLY:
    pass

class FUNC_DEF:
    pass

class RETURN:
    pass

class IMPORT:
    pass

class CALL_LIB_FUNC:
    pass

#中置演算子等
class CALC:
    pass

class CALL_FUNC:
    pass

#postfix operators, suck as ++ or --
class POSTFIX:
    pass

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

