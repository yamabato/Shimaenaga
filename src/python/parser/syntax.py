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
    self.statement = None

#variable definition
class VAR_DEF:
    def __init__(self, name=None, var_type=None, expr=None):
        self.name = None
        self.type = None
        self.expr = None

class ASSIGNMENT:
    pass

class COUNT_LOOP:
    pass

class INFINIT_LOOP:
    pass

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
        self.left = None
        self.right = None
        self.oper = None

class INTEGER:
    pass

class FLOAT:
    pass

class IDENT:
    pass

class STRING:
    pass

class BOOL:
    pass

class LIST:
    pass

class MAP:
    pass

