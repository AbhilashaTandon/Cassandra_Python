import lex_parse
import syn_parse
from expr import Expr
from symbol_table import SymbolTable
import sys
import main


def test_syntax_error():
    assert main.interpret('x') == SyntaxError
    assert main.interpret('var x') == SyntaxError
    assert main.interpret('var =') == SyntaxError
    assert main.interpret('fun') == SyntaxError
    assert main.interpret('fun is') == SyntaxError
    assert main.interpret('fun var') == SyntaxError        
    assert main.interpret('var fun') == SyntaxError        
    assert main.interpret('var var') == SyntaxError
    assert main.interpret('var var var var var') == SyntaxError
    assert main.interpret('var var = 2') == SyntaxError
    assert main.interpret('var fun = 2') == SyntaxError
    assert main.interpret('var calc = 2') == SyntaxError
    assert main.interpret('fun f(x,y) = x+y') != SyntaxError
    
print(main.debug("fun f(x,y) = x+y"))