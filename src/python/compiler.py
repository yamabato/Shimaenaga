#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print
from generator.gen_yse import generator
from gen_py.gen import gen_executable_code

code = """
i <- (10 + 20) * 20 + i
a <- 10 + 20
"""

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

#pretty_print(tree)

python_code = gen_executable_code(tree)
print(python_code)

#yse_code = generator(tree)
#print(yse_code)
