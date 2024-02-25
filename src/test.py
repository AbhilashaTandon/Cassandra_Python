import lex_parse

tests = [
    "3 * 5 - 100 / sin(e / log(343 * (2 + 2^(1.1 - tan(30)))))",
    """var x = 2
        fun f(x, y) = x^2 + y
        sim 3 - 3 * x + 5 * f(x, 2) - x
        calc der f(x,y) x
        calc grad f(x,y)"""
]

for test in tests:
    print()
    print(lex_parse.token_split(test))
