from expr import Expr
from language_spec import Variable, Function


class SymbolTable:
    variables: dict
    functions: dict

    def __init__(self):
        self.variables = {}
        self.functions = {}

    def __str__(self):
        out = "Variables: "
        for var in self.variables:
            out += str(self.variables[var]) + ", "
        out += "\nFunctions: "
        for fun in self.functions:
            out += str(self.functions[fun]) + ", "
        return out

    def check_for_uninitialized_symbols(self, expr):
        return SymbolTable.check_for_uninitialized_symbols(expr, self.variables, self.functions)

    def check_for_uninitialized_symbols(expr, variables, functions):
        for node in expr.get_nodes():
            if (node == "FUN" and node.name not in functions):
                raise NameError(
                    "function %s is not defined", node.name)  # if we use function in our definition that hasnt been defined
            if (node.type_ == "SYM" and node.name not in variables):
                raise NameError("variable %s is not defined", node.name)

    def add_var(self, var_name: str, expr: Expr):
        if(var_name in self.variables):
            raise NameError("redefinition of variable %s", var_name)
        SymbolTable.check_for_uninitialized_symbols(
            expr, self.variables.keys(), self.functions.keys())
        self.variables[var_name] = Variable(var_name, expr)

    def add_fun(self, fun_name, args, expr):
        # functions have 2 attribs, their arguments and their output
        if(fun_name in self.functions):
            raise NameError("redefinition of variable %s", fun_name)
        initialized_vars = self.variables.keys().copy()
        for x in args:
            initialized_vars.append(x)

        SymbolTable.check_for_uninitialized_symbols(
            expr, initialized_vars, self.functions.keys())

        self.functions[fun_name] = Function(
            name=fun_name, args=args, expr=expr, num_args=len(args))
        # arguments and
