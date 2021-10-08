#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print
from generator.gen_yse import generator

code = """
i <- 10 + 20 * 30
a <- 10
"""

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

pretty_print(tree)

yse_code = generator(tree)
print(yse_code)
