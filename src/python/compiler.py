#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser

code = """
i: integer <- 10
"""

code = "i: integer <- "

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()
