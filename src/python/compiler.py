#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print

code = """
func fib(n: integer)(integer){
    write(1*2*(3+(4+5)) + i)
}
write("ABC")
write(true)
"""

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

pretty_print(tree)
