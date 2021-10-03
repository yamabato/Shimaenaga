#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print

code = """
loop {
    i <- (1 + 2) * 3
    loop 10{
        i <- 10
        r <- 10
    }
}
"""


tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

print(tree.statements)

pretty_print(tree)
