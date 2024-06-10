import lex_parse
import syn_parse
from expr import Expr
from symbol_table import SymbolTable
import sys


def get_args(arg_list: list):  # converts string in form (x,y) to list of symbol arguments
    # each member will be a list of tokens in each argument (sequence separated by commas)
    arguments = []
    error = SyntaxError(
        "function arguments must be a list of symbols separated by commas, enclosed by parentheses")

    splitted_list = []
    for x in arg_list:
        if (x.name == ')'):

            arguments.append(splitted_list)
            break
        elif (x.name == ','):
            arguments.append(splitted_list)
            splitted_list = []
        else:
            splitted_list.append(x)

    args_out = []

    for x in arguments:
        if (len(x) != 1):  # should be only one token between commas
            raise error
        if (x[0].type_ != "SYM"):  # tokens cal only be symbol
            raise error
        else:
            args_out.append(x[0])

    return arguments


def parse(line: str, symbol_table: SymbolTable):
    print()
    print(line)
    tokens = lex_parse.lex_parse(line)
    command = tokens[0]

    # storing variables

    match command.name:  # which command
        case "var":
            var_name = tokens[1]
            if (var_name.type_ != "SYM"):  # if we didnt read the token after var as a symbol name
                raise SyntaxError(
                    "%s is not a valid symbol name" % var_name.name)
            if (tokens[2].type_ != '='):
                raise SyntaxError(
                    'variable initialization must start with "var", followed by the variable name, an equals sign, and an expression.')
            postfix = syn_parse.to_postfix(tokens[3:])
            expr = Expr(syn_parse.make_tree(postfix, symbol_table))

            symbol_table.add_var(var_name.name, expr)
        case "fun":
            fun_name = tokens[1]
            if (fun_name.type_ != "FUN"):  # if we didnt read the token after fun as a function name
                raise SyntaxError(
                    "%s is not a valid symbol name" % fun_name.name)
            if (tokens[2].name != '('):
                raise SyntaxError(
                    'function initialization must start with fun, followed by the function name, a list of arguments enclosed by parentheses, an equals sign, and an expression')

            print(get_args(tokens[3:]))

    print(symbol_table)

    # syntactic parsing
    # postfix = syn_parse.to_postfix(tokens)
    # print(postfix)
    # expr = Expr(syn_parse.make_tree(postfix, symbol_table))

    # print(expr)


def interpret(source_code: str):
    sym_tab = SymbolTable()
    for idx, line in enumerate(source_code.splitlines()):
        # try:
        #     parse(line, sym_tab)
        # except Exception:
        #     error = sys.exc_info()[0]
        #     error_message = sys.exc_info()[1]
        #     print("Line number %d: %s\t%s: %s" %
        #           (idx, line, str(error), error_message))
        #     return
        parse(line, sym_tab)


tests = [
    """var x = 2
    var y = csc(3 * sin(14.8 * pi / x) - 4^x^(x * 0.001 / e ^ sqrt(30) - 200 * ln(x)))
    fun f(x,d) = x + y"""]

for test in tests:

    interpret(test)

'''
var x = 2       [(LIT 2)]
var y = csc(3 * sin(14.8 * pi / x) - 4^x^(x * 0.001 / e ^ sqrt(30) - 200 * ln(x)))
[(LIT 3), (LIT 14.8), pi, *, (SYM x), /, sin, *, (LIT 4), (SYM x), (SYM x), (LIT 0.001), *, e, (LIT 30), sqrt, ^, /, (LIT 200), (SYM x), ln, *, -, ^, ^, -, csc]
'''
