"""
Boat AST Runner

Copyright 2023 chhongzh

MIT License
"""

from boat.type import BUILTINS
from boat.statement import *
from boat.lib_runner import *
from stdlib.builtin import _print, _input, _toint


class Runner(object):
    """
    AST node runner.
    """

    def __init__(self, module: Module):
        """
        A runner for Boat.
        Args:
            module:Module AST node root.
        """

        self.module = module
        self.ctx = CTX()  # Init variable context.
        self.function_ctx = FunctionCTX()  # Init function context.

    def run_statements(self, statements, ctx: CTX, function_ctx: FunctionCTX):
        """
        Run some statements.
        Args:
            statements to run
        """

        for statement in statements:
            if isinstance(statement, FunctionDef):
                function_ctx.new_function(statement)  # Add the function to the context.
            elif isinstance(statement, WhileStatement):
                while self.expr(statement.test, ctx, function_ctx):
                    self.run_statements(
                        statement.body, ctx, function_ctx
                    )  # Run WhileStatement body.
            elif isinstance(statement, VarAssignment):
                ctx[statement.name] = self.expr_assignment(statement, ctx, function_ctx)
            elif isinstance(statement, VarDef):
                if ctx.is_it_in(statement.name):
                    error_message(f'Var "{statement.name}" have been define.')
                ctx[statement.name] = None  # Create the new variable
            elif isinstance(statement, Call):
                self.expr_call(statement, ctx, function_ctx)  # Call the functions.
            elif isinstance(statement, ReturnStatement):
                return self.expr(
                    statement.val, ctx, function_ctx
                )  # Return it to the top.
            elif isinstance(statement, Compare):
                return self.expr_compare(
                    statement, ctx, function_ctx
                )  # Return the result to the top.
            elif isinstance(statement, IfStatement):
                self.expr_if(statement, ctx, function_ctx)

        return None  # For the non return function

    def run(self):
        """
        Run the root module.
        """
        self.run_statements(self.module.body, self.ctx, self.function_ctx)

    def expr(self, statement, ctx: CTX, function_ctx: FunctionCTX):
        # To express the expression
        if isinstance(statement, Var):
            if not ctx.is_it_in(statement.var):
                error_message(
                    f'Var "{statement.var}" not define.'
                )  # [ERROR] Not define
            return ctx[statement.var]
        elif isinstance(statement, BinOp):
            val = statement.calc(ctx, function_ctx, self.expr)
            return val

        elif isinstance(statement, Call):
            return self.expr_call(statement, ctx, function_ctx)
        elif isinstance(statement, Compare):
            return statement.compare(ctx, function_ctx, self.expr)
        else:
            return statement

    def expr_if(self, statement: IfStatement, ctx: CTX, function_ctx: FunctionCTX):
        tests = statement.tests
        bodys = statement.bodys

        if len(tests) > len(bodys):
            error_message("Test count bigger than Body count.")

        if len(tests) + 1 == len(bodys):  # if ..elif else:
            for test, body in zip(tests, bodys[:-1]):
                if self.expr(test, ctx, function_ctx):
                    self.run_statements(body, ctx, function_ctx)
                    break
            else:
                self.run_statements(bodys[-1], ctx, function_ctx)
        else:  # if ..elif
            for test, body in zip(tests[:-1], bodys[:-1]):
                if self.expr(test, ctx, function_ctx):
                    self.run_statements(body, ctx, function_ctx)
                    break

    def expr_assignment(
        self, statement: VarAssignment, ctx: CTX, function_ctx: FunctionCTX
    ):
        if not ctx.is_it_in(statement.name):
            error_message(f'Var "{statement.name}" not define.')
        else:
            val = self.expr(statement.var, ctx, function_ctx)
            # ctx.setitem(statement.name, val)
            return val

    def expr_compare(self, compare: Compare, ctx: CTX, function_ctx: FunctionCTX):
        return compare.compare(ctx, function_ctx, self.expr)

    def expr_args(self, args, ctx: CTX, function_ctx: FunctionCTX):
        for arg_index in range(len(args)):
            args[arg_index] = self.expr(args[arg_index], ctx, function_ctx)
        return args

    def expr_call(self, statement: Call, ctx: CTX, function_ctx: FunctionCTX):
        if statement.name in BUILTINS:
            if statement.name == "print":
                return _print(
                    *self.expr_args(statement.args, ctx, function_ctx)
                )  # Hook for the built in functions
            elif statement.name == "input":
                return _input(
                    *self.expr_args(statement.args, ctx, function_ctx)
                )  # Hook for the built in functions
            elif statement.name == "toint":
                return _toint(*self.expr_args(statement.args, ctx, function_ctx))
        elif function_ctx.is_it_in(statement.name):  # Check the function in the define.
            statement: Call
            function_ctx: list[FunctionDef]

            function_statement = function_ctx[statement.name]
            function_statement: FunctionDef

            temp_ctx = CTX()
            temp_function_ctx = FunctionCTX()

            for key, value in zip(
                function_statement.args,
                self.expr_args(statement.args, ctx, function_ctx),
            ):
                temp_ctx[key] = value

            return self.run_statements(
                function_statement.body, temp_ctx, temp_function_ctx
            )  # Need get value so return it.
        else:
            error_message(f'Function "{statement.name}" not define.')


if __name__ == "__main__":
    from test import CODE

    r = Runner(CODE)
    r.run()
