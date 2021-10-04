#encoding: utf-8

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../const"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../lexer"))

from .syntax import *
from token_type import *
from token_class import Token

class Parser:
    def __init__(self, tokens):
        self.cur_token = tokens
        self.peek_token = tokens.next_token

        self.error_occured = False

        self.left_brace = 0
        self.right_brace = 0


    def error(self):
        self.error_occured = True
        print("Error!!")

    def next(self):
        self.cur_token = self.peek_token

        if self.cur_token is None:
            self.cur_token = Token(EOP, EOP, None)

        if self.cur_token.next_token is None:
            self.peek_token = Token(EOP, EOP, None)
        else:
            self.peek_token = self.cur_token.next_token

    def skip_new_lines(self):
        while True:
            if self.cur_token.value != "\n": break

            self.next()
            
    #cur_tokenは最後にパースした構文の最後にセットしておく

    def parse_expression(self):
        left = self.parse_expr()

        self.next()
        if self.cur_token.value in COMP_OPER:
            oper = self.cur_token.value
        else:
            return left
        
        self.next()
        right = self.parse_expression()

        return EXPR(left, oper, right)

    def parse_expr(self):
        e = self.parse_term()
        while True:
            if self.peek_token.value in ["+", "-"]:
                self.next()
                oper = self.cur_token.value
                self.next()
                right = self.parse_term()
                e = EXPR(e, oper, right)
                continue
            else:
                return e

    def parse_term(self):
        e = self.parse_factor()

        while True:
            if self.peek_token.value in ["*", "/", "%", "//"]:
                self.next()
                oper = self.cur_token.value
                self.next()
                right = self.parse_factor()
                e = EXPR(e, oper, right)
                continue
            else:
                return e#!!!

    def parse_factor(self):
        if self.cur_token.value == "(":
            self.next()
            e = self.parse_expression()
            if self.cur_token.value == ")":
                #self.next()
                pass
            return e

        elif self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value == "(":
            v = self.parse_call_func()

        elif self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value == "@":
            v = self.parse_call_lib_func()
        
        else:
            v = self.parse_value()
        return v

    def parse_value(self):
        if self.cur_token.type == TYPE_INTEGER:
            return INTEGER(int(self.cur_token.value))

        if self.cur_token.type == TYPE_FLOAT:
            return FLOAT(float(self.cur_token.value))

        if self.cur_token.type == TYPE_STRING:
            return STRING(self.cur_token.value)

        if self.cur_token.type == TYPE_BOOL:
            return BOOL(self.cur_token.value)

        if self.cur_token.type == TYPE_IDENTIFIER:
            return IDENT(self.cur_token.value)
    
    def parse_var_def(self):
        name = self.cur_token.value

        self.next()
        self.next()

        var_type = self.cur_token.value
        if self.cur_token.type != TYPE_TYPE_KEYWORD:
            return None

        self.next()

        node = VAR_DEF()
        node.name = name
        node.type = var_type

        if self.cur_token.value == "\n":
            return node

        if self.cur_token.value != "<-":
            return None

        self.next()

        node.expr = self.parse_expression()

        return node

    def parse_assignment(self):
        name = self.cur_token.value

        self.next()
        self.next()

        expr = self.parse_expression()

        node = ASSIGNMENT(name, expr)

        return node

    def parse_count_loop(self):
        self.next()

        n = self.parse_expression()

        if self.cur_token.value != "{":
            return None

        st = self.parse()

        return COUNT_LOOP(n, st)

    def parse_infinit_loop(self):
        self.next()

        st = self.parse()

        return INFINIT_LOOP(st)

    def parse_break(self):
        self.next()
        return BREAK()

    def parse_continue(self):
        self.next()
        return CONTINUE()

    def parse_branch(self):
        self.next()
        self.next()

        node = BRANCH()
        if_condition = self.parse_expression()

        if self.cur_token.value != ")":
            return None
        if self.peek_token.value != "{":
            return None

        self.next()

        if_st = self.parse()
        
        if_clause = IF(if_condition, if_st)

        node.if_clause = if_clause
        
        elif_clauses = ELIF_CLAUSES()

        self.skip_new_lines()
        while True:
            if self.cur_token.value == "\n":
                self.next()
                continue
                
            if self.cur_token.value == "elif":
                if self.peek_token.value != "(":
                    return None

                self.next()
                condition = self.parse_expression()

                if self.cur_token.value != "{":
                    return None
                
                st = self.parse()

                elif_clause = ELIF(condition, st)
                elif_clauses.add_clause(elif_clause)

            else:
                break
        if elif_clauses.elif_clauses != []: node.elif_clauses = elif_clauses

        else_clause = ELSE()

        self.skip_new_lines()
        if self.cur_token.value == "else":
            self.next()

            if self.cur_token.value != "{":
                return None

            st = self.parse()

            else_clause.statements = st
            node.else_clause = else_clause


        return node

    def parse_switch_condition(self):
        self.next()
        self.next()
        
        node = SWITCH_CONDITION()
        match_clauses = MATCH_CONDITION_CLAUSES([])

        while True:
            if self.cur_token.value == "\n":
                self.next()
                continue

            elif self.cur_token.value in ["else", "finally"]:
                break

            if self.cur_token.value != "case" or self.peek_token.value != "(": return None
            self.next()
            self.next()

            condition = self.parse_expression()
            self.next()

            if self.cur_token.value != "{":
                return None

            st = self.parse()
            
            match_clause = MATCH_CONDITION(condition, st)
            match_clauses.add_match_condition_clause(match_clause)

        node.case_clauses = match_clauses

        if self.cur_token.value == "else":
            self.next()
            if self.cur_token.value != "{": return None
            
            st = self.parse()
            else_clause = ELSE(st)
            node.else_clause = else_clause

        elif self.cur_token.value != "{":
            return None

        self.skip_new_lines()

        if self.cur_token.value == "finally":
            self.next()
            if self.cur_token.value != "{": return None

            st = self.parse()
            finally_clause = FINALLY(st)
            node.finally_clause = finally_clause

        return node


    def parse_switch_value(self):
        self.next()

        value = self.parse_expression()

        if self.cur_token.value != "{": return None
        self.next()

        node = SWITCH_VALUE()
        node.value = value

        match_clauses = MATCH_VALUE_CLAUSES([])

        while True:
            self.skip_new_lines()
            if self.cur_token.value == "\n":
                self.next()
                continue

            elif self.cur_token.value in ["else", "finally_clause"]:
                break

            if self.cur_token.value != "case": return None
            self.next()

            exprs = EXPRS([])

            while True:
                expr = self.parse_expression()
                exprs.add_expr(expr)

                if self.cur_token.value == "{":
                    break

                if self.cur_token.value != ",": return None
                self.next()

            st = self.parse()

            match_clauses.add_match_value_clause(MATCH_VALUE(exprs, st))

        node.case_clauses = match_clauses

        if self.cur_token.value == "else":
            self.next()
            if self.cur_token.value != "{": return None

            st = self.parse()
            node.else_clause = ELSE(st)

        self.skip_new_lines()

        if self.cur_token.value == "finally":
            self.next()
            if self.cur_token.value != "{": return None

            st = self.parse()
            node.finally_clause = FINALLY(st)

        return node

    def parse_return(self):
        self.next()

        node = RETURN()
        if self.cur_token.value == "\n":
            return node

        exprs = EXPRS()
        while True:
            if self.cur_token.value == "\n":
                break

            expr = self.parse_expression()
            exprs.add_expr(expr)

            print(self.cur_token.value)
            if self.cur_token.value == ",":
                self.next()
                pass
            else:
                break

        node.exprs = exprs
        return node

    def parse_import(self):
        self.next()
        
        node = IMPORT()

        while True:
            if self.cur_token.type != TYPE_IDENTIFIER:
                return None

            node.add_name(self.cur_token.value)

            self.next()
            if self.cur_token.value == "\n":
                break

            if self.cur_token.value != ",":
                return None

            self.next()

        return node

    def parse_func_def(self):
        self.next()

        node = FUNC_DEF()

        name = self.cur_token.value
        node.name = name

        self.next()
        if self.cur_token.value != "(": return None
        self.next()
        
        args = []
        while True:
            if self.cur_token.value == ")": break
                
            if self.cur_token.type != TYPE_IDENTIFIER: return None
            arg_name = self.cur_token.value
            self.next()

            if self.cur_token.value != ":": return None
            self.next()

            if self.cur_token.type != TYPE_TYPE_KEYWORD: return None
            arg_type = self.cur_token.value
            self.next()

            args.append((arg_name, arg_type))
            if self.cur_token.value == ",":
                self.next()
                continue

            if self.cur_token.value != ")": return None

        self.next()
        node.arg_names = args


        if self.cur_token.value != "(": return None
        self.next()

        return_names = []
        while True:
            if self.cur_token.value == ")": break
                
            if self.cur_token.type != TYPE_IDENTIFIER: return None
            return_name = self.cur_token.value
            self.next()

            if self.cur_token.value != ":": return None
            self.next()

            if self.cur_token.type != TYPE_TYPE_KEYWORD: return None
            return_type = self.cur_token.value
            self.next()

            return_names.append((return_name, return_type))
            if self.cur_token.value == ",":
                self.next()
                continue

            if self.cur_token.value != ")": return None

        node.return_names = return_names

        self.next()
        st = self.parse()
        node.statements = st

        return node



    def parse_call_func(self):
        name = self.cur_token.value
        self.next()
        self.next()

        node = CALL_FUNC(name)
        args = ARGS([])

        while True:
            if self.cur_token.value == ")":
                break

            arg = self.parse_expression()
            args.add_arg(arg)

            if self.cur_token.value == ",":
                self.next()

            elif self.cur_token.value != ")":
                return None

        if args.args != []: node.args = args
        self.next()

        return node

    def parse_call_lib_func(self):
        name = self.cur_token.value
        self.next()
        self.next()

        if self.cur_token.type != TYPE_IDENTIFIER:
            return None

        lib = self.cur_token.value

        self.next()

        if self.cur_token.value != "(":
            return None
        self.next()

        args= ARGS([])
        while True:
            if self.cur_token.value == ")":
                break

            arg = self.parse_expression()
            args.add_arg(arg)

            if self.cur_token.value == ",":
                self.next()

            elif self.cur_token.value != ")":
                return None

        node = CALL_LIB_FUNC(name, lib)
        if args.args != []: node.args = args

        return node

    def parse_postfix(self):
        name = self.cur_token.value
        self.next()

        oper = self.cur_token.value

        node = POSTFIX(name, oper)

        return node
                
    def parse(self):
        tree = COMPOUND_STATEMENT()

        diff = self.left_brace - self.right_brace

        while True:
            st = None

            if self.error_occured:
                print("ERROR")
                break

            if self.cur_token.value == EOP: break
            if self.cur_token is None: break
            if self.cur_token.type == "" and self.cur_token.value is None:
                self.next()
                continue

            if self.cur_token.value == "{":
                self.left_brace += 1
                self.next()
                continue

            if self.cur_token.value == "}":
                self.right_brace += 1
                if self.left_brace - self.right_brace == diff:
                    self.next()
                    break

            if self.cur_token.value == "\n":
                self.next()
                continue

            #var: type [<- value] ;var_def 
            if self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value == ":":
                st = self.parse_var_def()

            #var <- expr ;assignment
            elif self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value == "<-":
                st = self.parse_assignment()

            elif self.cur_token.value == "loop" and self.peek_token.value != "{":
                st = self.parse_count_loop()

            elif self.cur_token.value == "loop" and self.peek_token.value == "{":
                st = self.parse_infinit_loop()

            elif self.cur_token.value == "break":
                st = self.parse_break()

            elif self.cur_token.value == "continue":
                st = self.parse_continue()

            elif self.cur_token.value == "if" and self.peek_token.value == "(":
                st = self.parse_branch()

            elif self.cur_token.value == "switch" and self.peek_token.value == "{":
                st = self.parse_switch_condition()
               
            elif self.cur_token.value == "switch" and self.peek_token.value != "{":
                st = self.parse_switch_value()

            elif self.cur_token.value == "return":
                st = self.parse_return()

            elif self.cur_token.value == "import":
                st = self.parse_import()

            elif self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value == "(":
                st = self.parse_call_func()

            elif self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value == "@":
                st = self.parse_call_lib_func()

            elif self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value in ["++", "--"]:
                st = self.parse_postfix()

            elif self.cur_token.value == "func" and self.peek_token.type == TYPE_IDENTIFIER:
                st = self.parse_func_def()

            else:
                print("!")
                self.next()
                continue

            if st is not None:
                tree.add_statement(st)

            else:
                print("ERROR")
                self.next()

        return tree

