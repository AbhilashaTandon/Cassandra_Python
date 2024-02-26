# builds Exprs, and checks syntax
from anytree import Node, RenderTree
from lex_parse import lex_parse, reserved_functions, reserved_constants, operators
from dataclasses import dataclass

# converts list of tokens from infix to postfix notation


def precedence(token):
    match token.value:
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
    return top_of_stack.value != '('


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
        name = token.value
        type_ = token.type_

        if (type_ in reserved_constants or type_ == "LIT" or type_ == "VARIABLE"):  # if constant or literal
            out_queue.append(token)
        elif (type_ in reserved_functions or type_ == "FUNCTION"):
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
                if (len(op_stack) > 0 and op_stack[-1].type_ == "FUNCTION"):
                    out_queue.append(op_stack.pop())
            else:
                o1 = token
                o1_prec = precedence(o1)
                while (len(op_stack) > 0 and not_left_paren_at_top(op_stack) and
                        ((precedence(op_stack[-1]) > o1_prec) or
                            (o1_prec == precedence(op_stack[-1]) and o1.value != "^"))):
                    out_queue.append(op_stack.pop())
                op_stack.append(o1)
    while (len(op_stack) > 0):
        if (not not_left_paren_at_top(op_stack)):
            raise SyntaxError("Misplaced Parentheses")
        out_queue.append(op_stack.pop())

    return out_queue


class Expr:
    root: Node

    def __init__(self, root: Node):
        self.root = root

    def equal(node1, node2):
        if (node1.value != node2.value):
            return False
        if (len(node1.children) != len(node2.children)):
            return False
        for child1, child2 in zip(node1.children, node2.children):
            if (not Expr.equal(child1, child2)):
                return False
        return True

    def __eq__(self, other):
        return Expr.equal(self.root, other.root)

    def __str__(self):
        str = ""
        for pre, _, node in RenderTree(self.root):
            str += ("%s%s\n" % (pre, node.name))
        return str

    def get_nodes_children(node: Node, node_list):
        for child in node.children:
            node_list.append(child)
            Expr.get_nodes_children(child, node_list)
        return node_list

    def get_nodes(self):
        nodes_list = []

        nodes_list.append(self.root)
        nodes_list = Expr.get_nodes_children(self.root, nodes_list)
        return nodes_list


@dataclass
class Function:
    name: str
    args: tuple
    expr: Expr
    num_args: int


class SymbolTable:
    variables: dict
    functions: dict

    def __init__(self):
        self.variables = {}
        self.functions = {}

    def check_for_uninitialized_symbols(expr, variables, functions):
        for node in expr.get_nodes():
            if (node.type_ == "FUNCTION" and node.value not in functions):
                raise NameError(
                    "function %s is not defined", node.value)  # if we use function in our definition that hasnt been defined
            if (node.type_ == "VARIABLE" and node.value not in variables):
                raise NameError("variable %s is not defined", node.value)

    def add_var(self, var_name: str, expr: Expr):
        SymbolTable.check_for_uninitialized_symbols(
            expr, self.variables.keys(), self.functions.keys())
        self.variables[var_name] = expr

    def add_fun(self, fun_name, args, expr):
        # functions have 2 attribs, their arguments and their output
        initialized_vars = self.variables.keys().copy()
        for x in args:
            initialized_vars.append(x)

        SymbolTable.check_for_uninitialized_symbols(
            expr, initialized_vars, self.functions.keys())

        self.functions[fun_name] = Function(
            name=fun_name, args=args, expr=expr, num_args=len(args))
        # arguments and


def make_tree(token_list, symbol_table: SymbolTable):  # converts postfix list into tree
    root = None
    tree_stack = []

    for x in token_list:
        args = x.num_args()  # num child arguments of node, 2 for op, 1 for func
        if (args == -1):  # we dont know args, must be custom function
            if (x.type_ == "FUNCTION"):
                if (x.value in symbol_table.functions.keys()):
                    args = symbol_table.functions[x.value].num_args
        children = []
        for arg in range(args):  # children are nodes at end of stack
            child = tree_stack.pop()  # pop from the end so children is reversed
            children.append(child)
        # we reverse it back here
        new_node = Node(name=x, children=children[::-1])
        if (len(tree_stack) == 0):  # update root,
            root = new_node
        tree_stack.append(new_node)
    return root
