#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser

code = """
loop {
    i <- 10 + 10
    loop 10{
        i <- 10
        r <- 10
    }
}
"""


tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

print(tree)
print(tree.statements)
