#encoding: utf-8

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../const"))

from .token_class import Token
from token_type import *

def add_token(token, tokens):
    if token not in IGNORE:
        token_type = check_token_type(token)
        value = eval_token(token, token_type)
        value = token
        t = Token(token_type, value, None)

        tokens.append(t)

def check_token_type(token):
    if token in SIGN_NAME:
        return TYPE_SIGN

    if token in KEYWORD:
        return TYPE_KEYWORD

    if token in KEYWORD_TYPE:
        return TYPE_TYPE_KEYWORD
 
    if token in BOOL_KEYWORD:
        return TYPE_BOOL
   
    if token.isdigit():
        return TYPE_INTEGER

    if token.replace(".", "", 1).isdigit():
        return TYPE_FLOAT

    if token[0] + token[-1] == "\"\"":
        return TYPE_STRING

    return TYPE_IDENTIFIER

def eval_token(token, token_type):
    if token_type == TYPE_SIGN:
        return token

    if token_type == TYPE_KEYWORD:
        return token

    if token_type == TYPE_BOOL:
        return BOOL_KEYWORD[token]

    if token_type == TYPE_INTEGER:
        return int(token)

    if token_type == TYPE_FLOAT:
        return float(token)

    if token_type == TYPE_STRING:
        return token[1:-1]

    return token

def lexer(code):
    tokens = []
    
    token = ""
    in_str = False
    in_comment = False
    n = 0
    code += " "

    while n < len(code):
        c = code[n]

        if in_comment:
            n += 1

            if c == "\n":
                in_comment = False

            continue

        if in_str:
            token += c
            n += 1

            if c in STR_SIGN:
                in_str = False

        else:
            for i in range(3, 0, -1):
                if code[n: n+i] in SIGN_NAME:
                    add_token(token, tokens)
                    token = ""
                    add_token(code[n: n+i], tokens)
                    n += len(code[n: n+i])

                    break
            else:
                if c in STR_SIGN:
                    add_token(token, tokens)
                    token = ""
 
                    in_str = True

                if c in COMMENT_SIGN:
                    add_token(token, tokens)
                    token = ""
 
                    in_comment = True
                    n += 1 
                    continue

                token += c
                n += 1

    eop = Token(EOP, EOP, None)
    tokens.append(eop)

    tokens = [Token()] + tokens

    head_token = tokens[0]
    cur_token = head_token

    for t in tokens[1:]:
        cur_token.next_token = t
        cur_token = cur_token.next_token

    return head_token
