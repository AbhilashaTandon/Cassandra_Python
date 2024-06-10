# specifies language parameters, classes, etc
from dataclasses import dataclass
import re

from collections import OrderedDict
from expr import Expr

# splits source code into tokens
# name must start with lowercase letter, have only lowercase letters and underscore, and be followed by parens
fun_regex = re.compile(r"[a-z][a-z0-9_]*\s*(?=\(.*\))")
# plus, minus, times, div, pow, left paren, right paren, comma
lit_regex = re.compile(r"[\d,]+[\d]\.?\d*|[\d,]*[\d]*\.?\d+")
symbol_regex = re.compile(r"[a-z][a-z0-9_]*")

function_paren = "(?=\(.*\))"

keywords = {  # reserved keywords in CASsandra
    "var": "VARIABLE",
    "fun": "FUNCTION",
    "calc": "CALCULATE",
    "sim": "SIMPLIFY",
    "der": "DERIVATIVE",
    "grad": "GRADIENT",
    "int": "INTEGRAL"
}

reserved_functions = ["sqrt", "cbrt", "log2", "log10",
                      "ln", "sin", "cos", "tan", "csc", "sec", "cot", "asin", "acos", "atan", "acsc", "asec", "acot"]
reserved_constants = ["pi", "e", "phi", "tau"]
operators = ["+", "-", "*", "/", "^", "=", '(', ')', ',']

token_res = OrderedDict()  # order is important for precendece
# each will be evaluated in turn, if match is found it will move forward in parsing str

token_res[re.compile(r'[\n\r]+')] = "EOF"

for keyword in keywords:  # first add keywords
    regex = re.compile(keyword)
    token_res[regex] = keywords[keyword]

for fun in reserved_functions:
    regex = re.compile(fun)
    token_res[regex] = fun

for const in reserved_constants:
    regex = re.compile(const)
    token_res[regex] = const

for op in operators:
    token_res[re.compile('\\' + op)] = op

token_res[fun_regex] = "FUN"
token_res[symbol_regex] = "SYM"

token_res[lit_regex] = "LIT"


@dataclass
class Token:  # each token we analyze in the source code sequence
    name: str
    type_: str
    num_args: int

    def __str__(self):
        if (self.name == self.type_):
            return self.name
        else:
            return "(%s %s)" % (self.type_, self.name)

    def __repr__(self):
        return self.__str__()

    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_
        if (type_ in operators):
            self.num_args = 2
        elif (type_ in reserved_constants):
            self.num_args = 0
        elif (type_ in reserved_functions):
            self.num_args = 1
        elif (type_ == "LIT"):
            self.num_args = 0
        elif (type_ == "FUN"):
            self.num_args = -1  # unknown num args
        else:
            self.num_args = 0

# classes for symbol table


@dataclass
class Function:
    name: str
    num_args: int
    args: list
    expr: Expr

    def __str__(self):
        out = ""
        out += self.name + "(" + ','.join(self.args) + ") : " + str(self.expr)
        return out


@dataclass
class Variable:
    name: str
    expr: Expr

    def __str__(self):
        out = ""
        out += self.name + " : " + str(self.expr)
        return out


def is_function(token: Token):
    if (token.type_ == "FUN"):
        return True
    if (token.name in reserved_functions):
        return True
    return False


def is_value(token: Token):
    if (token.type_ == "LIT" or token.type_ == "SYM"):
        return True
    if (token.name in reserved_constants):
        return True
    return False
