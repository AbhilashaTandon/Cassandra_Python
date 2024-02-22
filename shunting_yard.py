from tokenizer import *
from anytree import Node, RenderTree


def is_left_paren(token):
    if (not isinstance(token, Operator)):
        return False
    return token.char == '('


def not_left_paren_at_top(op_stack):
    if (len(op_stack) == 0):
        return True
    top_of_stack = op_stack[-1]
    if (not isinstance(top_of_stack, Operator)):
        return True
    return top_of_stack.char != '('


def shunting_yard(token_list):
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
                    if (len(op_stack) != 0):
                        raise SyntaxError("Misplaced Parentheses")
                    out_queue.append(op_stack.pop())
                assert (not not_left_paren_at_top(op_stack))
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


def make_tree(node_list):
    tree_stack = []

    for x in node_list:
        print(tree_stack)
        if (len(tree_stack) == 0):
            tree_stack.append(Node(x))
        else:
            while len(tree_stack) > 0:
                last_node = tree_stack[-1]
                num_args = last_node.name.num_args()
                num_children = len(last_node.children)
                if (num_children < num_args):
                    tree_stack.append(Node(x, parent=last_node))
                else:
                    tree_stack.pop()  # remove finished nodes from list
