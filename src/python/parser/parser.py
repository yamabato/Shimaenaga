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
            return left #!!!
        
        self.next()
        right = self.parse_expression()

        return "(" + left + oper + right + ")"#!!!

    def parse_expr(self):
        e = self.parse_term()
        while True:
            if self.peek_token.value in ["+", "-"]:
                self.next()
                oper = self.cur_token.value
                self.next()
                right = self.parse_term()
                e = "(" + e + oper + right + ")" #!!!
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
                e = "(" + e + oper + right + ")" #!!!
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

        return self.cur_token.value
    
    def parse_var_def1(self):
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

        print(node.expr)
        return node
        
    def parse(self):
        tree = COMPOUND_STATEMENT()

        while True:
            st = None

            if self.error_occured: break

            if self.cur_token.value == EOP: break
            if self.cur_token is None: break
            
            #var: type [<- value];var_def1 
            if self.cur_token.type == TYPE_IDENTIFIER and self.peek_token.value == ":":
                st = self.parse_var_def1()

                if st is not None:
                    tree.add_statement(st)

            else:
                self.next()


        print(tree.statements)

