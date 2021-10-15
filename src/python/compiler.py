#encoding: utf-8

from preprocessor.preprocessor import preprocessor
from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print
from generator.gen_yse import generator
from gen_py.gen import gen_executable_code

import os
import sys

code = """
b: bool <- 1 == 1
"""

fn = ""
if len(sys.argv) == 2:
    fn = sys.argv[1]

    if os.path.isfile(fn) and fn[-3:] == ".se":
        with open(fn, mode="r") as f:
            code = f.read()

    else:
        fn = ""

added = True
lib_name = []
while added:
    code, added, lib_name = preprocessor(code, lib_name)

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

#pretty_print(tree)

python_code = gen_executable_code(tree)
#print(python_code)

file_name = "output.py"
if fn != "":
    file_name = "".join(fn.split(".")[:-1]) + ".py"
with open(file_name, mode="w", encoding="utf-8") as f:
    f.write(python_code)

#yse_code = generator(tree)
#print(yse_code)
