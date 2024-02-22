import tokenizer
import shunting_yard
from expression import Expression

tests = ["3 * 5 - 100 / sin(e / log(343 * (2 + 2^(1.1 - tan(30)))))"]

for test in tests:
    tree1 = Expression(test)
    print(tree1.evaluate())
