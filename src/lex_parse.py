import re
from dataclasses import dataclass
from collections import OrderedDict

# splits source code into tokens
# name must start with lowercase letter, have only lowercase letters and underscore, and be followed by parens
fun_regex = re.compile(r"[a-z][a-z0-9_]+(?=\(.*\))")
# plus, minus, times, div, pow, left paren, right paren, comma
lit_regex = re.compile(r"[\d,]+\.?\d*|[\d,]*\.?\d+")
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
                      "ln", "log", "sin", "cos", "tan", "csc", "sec", "cot", "asin", "acos", "atan", "acsc", "asec", "acot"]
reserved_constants = ["pi", "e", "phi", "tau"]
operators = ["+", "-", "*", "/", "^", "=", '(', ')', ',']

token_res = OrderedDict()  # order is important for precendece
# each will be evaluated in turn, if match is found it will move forward in parsing str

token_res[re.compile(r'[\n\r]+')] = "EOF"

for keyword in keywords:  # first add keywords
    regex = re.compile(keyword)
    token_res[regex] = keywords[keyword]

token_res[tuple_regex] = "TUPLE"

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

for token in token_res:
    print(token, token_res[token])


def lex_parse(expr: str):
    expr = expr.lower()
    tokens = []
    idx = 0
    while (idx < len(expr)):
        current_slice = expr[idx:]

        matches = [regex.search(current_slice) for regex in token_res]

        new_token = None
        # dummy string has len 1 so idx will advance by 1 char each iter if none found
        match_str: str = " "
        # the order of these is important, in cases of multiple matches first one takes precedence

        for match, type_ in zip(matches, token_res.values()):
            if (match is not None and match.start() == 0):
                match_str = str(match.group(0))
                new_token = (match_str, type_)
                break
        idx += len(match_str)
        if (new_token is not None):
            tokens.append(new_token)
    return tokens
