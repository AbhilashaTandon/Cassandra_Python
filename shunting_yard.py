from tokenizer import *
from anytree import Node, RenderTree


def is_left_paren(token):  # check if op is left paren
    # this function is just to make shunting yard more concise
    if (not isinstance(token, Operator)):
        return False
    return token.char == '('


def not_left_paren_at_top(op_stack):
    # this function is just to make shunting yard more concise
    if (len(op_stack) == 0):
        return True
    top_of_stack = op_stack[-1]
    if (not isinstance(top_of_stack, Operator)):
        return True
    return top_of_stack.char != '('


def shunting_yard(token_list):
    # implements shunting yard algorithm
    # https://en.wikipedia.org/wiki/Shunting_yard_algorithm
    if (len(token_list) < 2):
        return token_list  # single token or none
    out_queue = []
    op_stack = []
    for x in token_list:
        if (isinstance(x, Constant)):
            out_queue.append(x)
        elif (isinstance(x, Literal)):
            out_queue.append(x)
        elif (isinstance(x, Function)):
            op_stack.append(x)
        elif (isinstance(x, Operator)):
            if (x.char == ','):
                while not_left_paren_at_top(op_stack):
                    out_queue.append(op_stack.pop())
            elif (is_left_paren(x)):
                op_stack.append(x)
            elif (x.char == ')'):
                while not_left_paren_at_top(op_stack):
                    if (len(op_stack) == 0):
                        raise SyntaxError("Misplaced Parentheses")
                    out_queue.append(op_stack.pop())
                if (not_left_paren_at_top(op_stack)):
                    raise SyntaxError("Misplaced Parentheses")
                op_stack.pop()
                if (len(op_stack) > 0 and isinstance(op_stack[-1], Function)):
                    out_queue.append(op_stack.pop())
            else:
                o1 = x
                while (len(op_stack) > 0 and not_left_paren_at_top(op_stack) and
                        ((op_stack[-1].precedence() > o1.precedence()) or
                         (o1.precedence() == op_stack[-1].precedence() and o1.left_assoc()))):
                    out_queue.append(op_stack.pop())
                op_stack.append(o1)
    while (len(op_stack) > 0):
        if (not not_left_paren_at_top(op_stack)):
            raise SyntaxError("Misplaced Parentheses")
        out_queue.append(op_stack.pop())

    return out_queue


def make_tree(node_list):  # converts postfix list into tree
    root = None
    tree_stack = []

    for x in node_list:
        args = x.num_args()  # num child arguments of node, 2 for op, 1 for func
        children = []
        for arg in range(args):  # children are nodes at end of stack
            child = tree_stack.pop()
            children.append(child)
        new_node = Node(name=x, children=children)
        if (len(tree_stack) == 0):  # update root,
            root = new_node
        tree_stack.append(new_node)
    if (root is not None):
        for pre, _, node in RenderTree(root):
            print("%s%s" % (pre, node.name))
    return root
