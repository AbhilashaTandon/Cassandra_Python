import tokenizer
import shunting_yard


def parse(expr):
    tokens = tokenizer.token_split(expr)

    tree = shunting_yard.shunting_yard(tokens)
    shunting_yard.make_tree(tree)


tests = ["()", "2 + 2", "9",
         "(((2 - 3 / sin(45.1341 - .120341 * 02. / (3 ^ e / pi * sqrt(10))))))"]
for x in tests:
    parse(x)
