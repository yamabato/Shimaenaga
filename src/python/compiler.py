#encoding: utf-8

from lexer.lexer import lexer
from parser.parser import Parser
from parser.pretty_print import pretty_print

code = """
switch i+2{
    case 2, 3{
        write()
    }

    case 4, 5{
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
