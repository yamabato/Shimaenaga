#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print

code = """
func f(a1: integer, a2: string)(a: integer){
    write(a1, a2)
}
write(a, 2)
i <- a + 1
"""

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

pretty_print(tree)
