#encoding: utf-8

SIGN_NAME = [
    " ",
    "\n",
    ",",
    ":",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    "<-",
    "->",
    "+",
    "-",
    "*",
    "/",
    "%",
    "|",
    "&",
    "^",
    "+=",
    "-=",
    "/=",
    "*=",
    "%=",
    "//=",
    "++",
    "--",
    "//",
    "@",
    "<",
    ">",
    "<=",
    ">=",
    "==",
    "!=",
    "^^",
]

KEYWORD = [
    #"#counter",

    "loop",
    "if",
    "elif",
    "else",
    "switch",
    "case",
    "finally",
    "break",
    "continue",
    "func",
    "return",
    "import",
]

KEYWORD_TYPE = [
    "integer",
    "float",
    "string",
    "list",
    "queue",
    "stack",
    "map",
    "bool",
]

COMP_OPER = [
    "<",
    ">",
    "<=",
    ">=",
    "==",
    "!=",
]

POSTFIX_OPER = [
    "++",
    "--",
]

STR_SIGN = ['"', "'"]
COMMENT_SIGN = [";"]
BOOL_KEYWORD = {"true": True, "false": False}

IGNORE = ["", " "]

TYPE_SIGN = "SIGN"
TYPE_KEYWORD = "KEYWORD"
TYPE_TYPE_KEYWORD = "TYPE"
TYPE_INTEGER = "INT"
TYPE_FLOAT = "FLOAT"
TYPE_STRING = "STRING"
TYPE_IDENTIFIER = "IDENT"
TYPE_BOOL = "BOOL"

EOP = "EOP"
