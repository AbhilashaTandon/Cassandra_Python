from language_spec import Token
import language_spec
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
    tokens = lex_parse.lex_parse(line)
    command = tokens[0]
    if(len(tokens) < 2):
        raise SyntaxError("line must have more than 2 tokens")

    # storing variables

    match command.name:  # which command
        case "var":
            var_name = tokens[1]
            if (var_name.type_ != "SYM"):  # if we didnt read the token after var as a symbol name
                raise SyntaxError(
                    "%s is not a valid symbol name" % var_name.name)
            if(len(tokens) < 4 or tokens[2].type_ != '='): #short circuiting should prevent index error
                raise SyntaxError(
                    'variable initialization must start with "var", followed by the variable name, an equals sign, and an expression.')
            postfix = syn_parse.to_postfix(tokens[3:])
            expr = Expr(syn_parse.make_tree(postfix, symbol_table))
            symbol_table.add_var(var_name.name, expr)
        
        
        case "fun":
            if(len(tokens) < 6):
                raise SyntaxError("function initialization must start with fun, followed by the function name, followed by a list of arguments enclosed by parenthesis, followed by an equals sign, and an expression")
            fun_name = tokens[1]
            if (fun_name.type_ != "FUN"):  # if we didnt read the token after fun as a function name
                raise SyntaxError(
                    "%s is not a valid symbol name" % fun_name.name)
            if (tokens[2].name != '('):
                raise SyntaxError(
                    'function initialization must have a list of arguments enclosed by parenthesis')
            
            args = get_args(tokens[3:])
            expr = None
            
            
            for i, token in enumerate(tokens): 
                if(token == language_spec.EQ): #find expr after equals sign
                    if(len(tokens) == i+1): #if ends w equal sign
                        raise SyntaxError('function initialization must have an expression following equals sign')
                    expr = Expr(syn_parse.make_tree(tokens[i+1:], symbol_table))
                    break
            
            if(expr is None):
                raise SyntaxError('function initialization must contain an equals sign')
            
            symbol_table.add_fun(fun_name, args, expr)
            
            
        
        case "calc":
            raise RuntimeError("not implemented")
        case "sim":
            raise RuntimeError("not implemented")
        case "der":
            raise RuntimeError("not implemented")
        case "grad":
            raise RuntimeError("not implemented")
        case "int":
            raise RuntimeError("not implemented")
        case _:
            raise SyntaxError("every line must begin with one of valid commands: var, fun, calc, sim, der, grad, int")
            

    return symbol_table

    # syntactic parsing
    # postfix = syn_parse.to_postfix(tokens)
    # print(postfix)
    # expr = Expr(syn_parse.make_tree(postfix, symbol_table))

    # print(expr)


def interpret(source_code: str):
    sym_tab = SymbolTable()
    for idx, line in enumerate(source_code.splitlines()):
        try:
            sym_tab = parse(line, sym_tab)
        except Exception:
            error = sys.exc_info()[0]
            error_message = sys.exc_info()[1]
            return error
    return sym_tab

def debug(source_code: str):
    sym_tab = SymbolTable()
    for idx, line in enumerate(source_code.splitlines()):
        try:
            sym_tab = parse(line, sym_tab)
        except Exception:
            error = sys.exc_info()[0]
            error_message = sys.exc_info()[1]
            print("Line number %d: %s\t%s: %s" %
                  (idx+1, line, str(error), error_message))
            return
        print(sym_tab)
    print(sym_tab)
    