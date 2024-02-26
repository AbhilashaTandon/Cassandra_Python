import lex_parse
import syn_parse

tests = ["(8 - 1 + 3) * 6 - ((3 + 7) * 2)",
         """
         var x = 2
         fun f(x, y) = x^2 + y
         comp f(x, 2) 3
         calc grad f(x,y)
         
         simp x + 3 - 3 / 1
         der x f(x, x)
         """]

for test in tests:
    print()
    tokens = lex_parse.lex_parse(test)
    sym_tab = syn_parse.SymbolTable()
    postfix = syn_parse.to_postfix(tokens)
    expr = syn_parse.Expr(syn_parse.make_tree(postfix, sym_tab))
    print(str(expr))
    for x in syn_parse.syn_parse(tokens):
        print(str(x))
    print()
