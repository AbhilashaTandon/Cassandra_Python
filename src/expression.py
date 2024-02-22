from dataclasses import dataclass
from anytree import Node, RenderTree
from shunting_yard import to_postfix, make_tree
from tokenizer import token_split, Literal, Operator, Function, Constant
import math


@dataclass
class Expression:
    root: Node

    def equal(node1, node2):
        if (node1.name != node2.name):
            return False
        if (len(node1.children) != len(node2.children)):
            return False
        for child1, child2 in zip(node1.children, node2.children):
            if (not Expression.equal(child1, child2)):
                return False
        return True

    def eval_node(node: Node):
        content = node.name
        if (isinstance(content, Literal)):
            return content.value
        elif (isinstance(content, Constant)):
            match content.char:
                case 'pi': return math.pi
                case 'tau': return math.tau
                case 'e': return math.e
                case 'phi': return 1.618033988749894
                case other: raise ValueError("Unrecognized constant %s" % content.char)
        elif (isinstance(content, Function)):
            argument = Expression.eval_node(node.children[0])
            match content.name:
                case 'sin': return math.sin(argument)
                case 'cos': return math.cos(argument)
                case 'tan': return math.tan(argument)
                case 'log': return math.log(argument)
                case 'log2': return math.log2(argument)
                case 'log10': return math.log10(argument)
                case 'ln': return math.ln(argument)
                case 'asin': return math.asin(argument)
                case 'acos': return math.acos(argument)
                case 'atan': return math.atan(argument)
                case 'csc': return math.csc(argument)
                case 'sec': return math.sec(argument)
                case 'cot': return math.cot(argument)
                case 'acsc': return math.acsc(argument)
                case 'asec': return math.asec(argument)
                case 'acot': return math.acot(argument)
                case other: raise ValueError("Unrecognized function %s" % content.name)
        elif (isinstance(content, Operator)):
            arg_1 = Expression.eval_node(node.children[0])
            arg_2 = Expression.eval_node(node.children[1])
            match content.char:
                case '+': return arg_1 + arg_2
                case '-': return arg_1 - arg_2
                case '*': return arg_1 * arg_2
                case "/":
                    if (arg_2 == 0):
                        raise ZeroDivisionError("Division by 0")
                    else:
                        return arg_1 / arg_2
                case "^": return arg_1 ** arg_2
                case other: raise ValueError("Unrecognized operator %s" % content.char)
        return None

    def evaluate(self):
        return Expression.eval_node(self.root)

    def simplify_node(node: Node):
        # returns node but simplifies its expression
        # uses arithmetic identities

        if (len(node.children) == 0):
            return node
        new_children = []
        for x in node.children:
            simple = Expression.simplify_node(x)
            new_children.append(simple)
        node.children = tuple(new_children)

        # do this first so simplifications cascade
        val = node.name

        if (val == Operator("*")):
            first, second = node.children[0], node.children[1]

            # 0 * x == 0
            if (first.name == Literal(0) or second.name == Literal(0)):
                new_node = Node(name=Literal(0))
                return new_node

            # 1 * x == x
            if (first.name == Literal(1)):
                return second
            elif (second.name == Literal(1)):
                return first

            if (Expression.equal(first, second)):
                new_node = Node(name=Operator("^"))
                new_node.children = (first, Node(name=Literal(2)))
                return new_node

        elif (val == Operator("+")):
            first, second = node.children[0], node.children[1]
            if (first.name == Literal(0)):
                return second
            elif (second.name == Literal(0)):
                return first

            if (Expression.equal(first, second)):
                new_node = Node(name=Operator("*"))
                new_node.children = (first, Node(name=Literal(2)))
                return new_node
        return node

    def __eq__(self, other):
        return Expression.equal(self.root, other.root)

    def __init__(self, expr: str):
        token_list = token_split(expr)
        postfix = to_postfix(token_list)
        tree = make_tree(postfix)
        self.root = tree

    def simplify(self):
        self.root = Expression.simplify_node(self.root)

    def __str__(self):
        str = ""
        for pre, _, node in RenderTree(self.root):
            str += ("%s%s\n" % (pre, node.name))
        return str
