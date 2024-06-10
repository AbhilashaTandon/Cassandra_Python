from anytree import Node, RenderTree


class Expr:
    root: Node

    def __init__(self, root: Node):
        self.root = root

    def equal(node1, node2):
        if (node1.name != node2.name):
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
        if (self.root is None):
            return str
        for pre, _, node in RenderTree(self.root):
            str += ("%s%s\n" % (pre, node.name))
        return str

    def get_nodes_children(node: Node, node_list):
        for child in node.children:
            node_list.append(child.name)
            Expr.get_nodes_children(child, node_list)
        return node_list

    def get_nodes(self):
        nodes_list = []

        nodes_list.append(self.root.name)
        nodes_list = Expr.get_nodes_children(self.root, nodes_list)
        return nodes_list
