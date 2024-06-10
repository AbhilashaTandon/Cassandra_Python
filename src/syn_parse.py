# builds Exprs, and checks syntax

from language_spec import *

from expr import Expr
from lex_parse import reserved_functions, reserved_constants, operators
from dataclasses import dataclass
from symbol_table import SymbolTable
from anytree import Node

# converts list of tokens from infix to postfix notation


def precedence(token):

    match token.name:
        case '^': return 4
        case '*': return 3
        case '/': return 3
        case '+': return 2
        case '-': return 2
        case other: return 0


def not_left_paren_at_top(op_stack):
    # this function is just to make to_postfix more concise
    if (len(op_stack) == 0):
        return True
    top_of_stack = op_stack[-1]
    return top_of_stack.name != '('


def to_postfix(token_list):
    # we need the symbol table to check how many arguments each function has
    # if no symbols have been initialized yet we shouldnt need to check
    # symbol table checks for uninitialized symbols so we dont here
    if (len(token_list) < 2):
        return token_list
    # if just 1 or 0 tokens no parsing needed

    out_queue = []
    op_stack = []
    for token in token_list:
        name = token.name
        type_ = token.type_

        if (is_value(token)):  # if constant or literal
            out_queue.append(token)
        elif (is_function(token)):
            op_stack.append(token)

        elif (type_ in operators):
            if (name == ','):
                while not_left_paren_at_top(op_stack):
                    out_queue.append(op_stack.pop())
            elif (name == '('):
                op_stack.append(token)
            elif (name == ')'):
                while not_left_paren_at_top(op_stack):
                    if (len(op_stack) == 0):
                        raise SyntaxError("Misplaced Parentheses")
                    out_queue.append(op_stack.pop())
                if (not_left_paren_at_top(op_stack)):
                    raise SyntaxError("Misplaced Parentheses")
                op_stack.pop()
                if (len(op_stack) > 0 and is_function(op_stack[-1])):
                    out_queue.append(op_stack.pop())
            else:
                o1 = token
                o1_prec = precedence(o1)
                while (len(op_stack) > 0 and not_left_paren_at_top(op_stack) and
                        ((precedence(op_stack[-1]) > o1_prec) or
                            (o1_prec == precedence(op_stack[-1]) and o1.name != "^"))):
                    out_queue.append(op_stack.pop())
                op_stack.append(o1)
    while (len(op_stack) > 0):
        if (not not_left_paren_at_top(op_stack)):
            raise SyntaxError("Misplaced Parentheses")
        out_queue.append(op_stack.pop())

    return out_queue


def make_tree(token_list, symbol_table: SymbolTable):  # converts postfix list into tree
    root = None
    tree_stack = []

    for x in token_list:
        args = x.num_args  # num child arguments of node, 2 for op, 1 for func
        if (args == -1):  # we dont know args, must be custom function
            if (x.type_ == "FUN"):
                if (x.name in symbol_table.functions.keys()):
                    args = symbol_table.functions[x.name].num_args
                else:
                    raise NameError("Unrecognized function %s" % x.name)
            else:
                raise Exception("Something very strange happened")
        children = []
        for _ in range(args):  # children are nodes at end of stack
            child = tree_stack.pop()  # pop from the end so children is reversed
            children.append(child)
        # we reverse it back here
        new_node = Node(name=x, children=children[::-1])
        if (len(tree_stack) == 0):  # update root,
            root = new_node
        tree_stack.append(new_node)
    return root
