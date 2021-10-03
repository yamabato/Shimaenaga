#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print

code = """
switch {
    case (1==2){
        write()
    }
    case (2+2 == 2){
        write()
    }
    else{
        write()
    }
    finally{
        write()
    }
}
loop {
    if (1==2){
        print()
    }
}
"""

tokens = lexer(code)
parser = Parser(tokens)
tree = parser.parse()

pretty_print(tree)
