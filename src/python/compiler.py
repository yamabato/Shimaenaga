#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print

code = """
import random, math table 
"""

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

pretty_print(tree)
