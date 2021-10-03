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

    def parse_branch(self):
        self.next()
        self.next()

        if_condition = self.parse_expression()

        if self.cur_token.value != ")":
            return None
        if self.peek_token.value != "{":
            return None

        self.next()

        if_st = self.parse()
        
        if_clause = IF(if_condition, if_st)
        
        elif_clauses = ELIF_CLAUSES()

        while True:
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

        else_clause = ELSE()

        if self.cur_token.value == "else":
            self.next()

            if self.cur_token.value != "{":
                return None

            st = self.parse()

            else_clause.statements = st

        node = BRANCH(if_clause, elif_clauses, else_clause)

        return node

    def parse_block(self):
        block_tokens = []
        
    def parse(self):
        tree = COMPOUND_STATEMENT()

        diff = self.left_brace - self.right_brace

        while True:
            st = None

            if self.error_occured: break

            if self.cur_token.value == EOP: break
            if self.cur_token is None: break
            if self.cur_token.type == "" and self.cur_token.value is None:
                self.next()
                continue

            if self.cur_token.value == "{":
                self.left_brace += 1

            if self.cur_token.value == "}":
                self.right_brace += 1
                if self.left_brace - self.right_brace == diff:
                    self.next()
                    break
            #var: type [<- value] ;var_def 
            if self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value == ":":
                print("VAR_DEF")
                st = self.parse_var_def()

            #var <- expr ;assignment
            elif self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value == "<-":
                print("ASSIGNMENT")
                st = self.parse_assignment()

            elif self.cur_token.value == "loop" and self.peek_token.value != "{":
                print("COUNT")
                st = self.parse_count_loop()

            elif self.cur_token.value == "loop" and self.peek_token.value == "{":
                print("INFINIT_LOOP")
                st = self.parse_infinit_loop()

            elif self.cur_token.value == "if" and self.peek_token.value == "(":
                print("BRANCH")
                st = self.parse_branch()

            if st is not None:
                tree.add_statement(st)

            else:
                self.next()

        return tree

