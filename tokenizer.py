import re
from dataclasses import dataclass


def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


fun_regex = re.compile(r"[a-z][a-z0-9_]+")
op_regex = re.compile(r"([+\-*/^\(\),]|log)")
const_regex = re.compile(r"pi|tau|phi|e")
lit_regex = re.compile(r"[\d,]+\.?\d*|[\d,]*\.?\d+")

regexes = [fun_regex, op_regex, const_regex, lit_regex]


class Token:
    num_args: int

    def parse(string: str):
        raise NotImplemented


@dataclass
class Literal(Token):
    value: float

    def __str__(self) -> str:

        return "Literal(%f)" % self.value

    def num_args(self) -> int:
        return 0


@dataclass
class Operator(Token):
    char: str

    def __str__(self) -> str:
        return "Operator(%s)" % self.char

    def precedence(self) -> int:
        match self.char:
            case '^': return 4
            case '*': return 3
            case '/': return 3
            case '+': return 2
            case '-': return 2
            case other: return 0
        return 0

    def left_assoc(self) -> bool:  # if op is left associative w/e that means
        if (self.char == '^'):
            return False
        return True

    def num_args(self) -> int:
        return 2


@dataclass
class Function(Token):
    name: str

    def __str__(self):
        return "Function(%s)" % self.name

    def num_args(self) -> int:
        return 1


@dataclass
class Constant(Token):
    char: str

    def __str__(self):
        return "Constant(%s)" % self.char

    def num_args(self) -> int:
        return 0


def token_split(expr: str):
    tokens = []
    idx = 0
    while (idx < len(expr)):
        current_slice = expr[idx:]
        fun_match = fun_regex.search(current_slice)
        op_match = op_regex.search(current_slice)
        const_match = const_regex.search(current_slice)
        lit_match = lit_regex.search(current_slice)
        new_token = None
        # dummy string has len 1 so idx will advance by 1 char each iter if none found
        match_str: str = " "
        # the order of these is important, in cases of multiple matches const, then op, then fun take precedence
        if (const_match is not None and const_match.start() == 0):
            match_str = str(const_match.group(0))
            new_token = Constant(match_str)
        elif (op_match is not None and op_match.start() == 0):
            match_str = str(op_match.group(0))
            new_token = Operator(match_str)
        elif (fun_match is not None and fun_match.start() == 0):
            match_str = str(fun_match.group(0))
            new_token = Function(match_str)
        elif (lit_match is not None and lit_match.start() == 0):
            match_str = str(lit_match.group(0))
            if (is_float(match_str)):
                new_token = Literal(float(match_str))
        idx += len(match_str)
        if (new_token is not None):
            tokens.append(new_token)
    return tokens
