#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print
from generator.gen_yse import generator
from gen_py.gen import gen_executable_code

code = """
i: integer
i <- 10 + 1
"""

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

#pretty_print(tree)

python_code = gen_executable_code(tree)
print(python_code)

file_name = "output.py"
with open(file_name, mode="w", encoding="utf-8") as f:
    f.write(python_code)

#yse_code = generator(tree)
#print(yse_code)
