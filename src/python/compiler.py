#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print

code = """
if (1+1 == 2){
    i <- 2
}elif(1 == 2){
    i <- 3
}else{
    i <- 0
}
"""

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

pretty_print(tree)
