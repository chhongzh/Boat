"""
Boat AST Runner

Copyright 2023 chhongzh

MIT License
"""

from .type import BUILTINS
from .statement import *
from .lib_runner import *
from .stdlib.builtin import _print, _input, _toint, _tostr, _tofloat
from .errors import *


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

    def run_statements(
        self, statements, ctx: CTX, function_ctx: FunctionCTX, catches=[]
    ):
        """
        Run some statements.
        Args:
            statements to run
        """

        for statement in statements:
            self.run_statement(statement, ctx, function_ctx, catches)

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
                NotDefineError(
                    f'Var "{statement.var}" not define.'
                ).raise_it()  # [ERROR] Not define
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

    def expr_raise(
        self, statement: RaiseStatement, ctx: CTX, function_ctx: FunctionCTX
    ):
        global ERRORS_MAP
        statement.expection: str
        ERRORS_MAP[statement.expection](
            *self.expr_args(statement.args, ctx, function_ctx)
        ).raise_it()

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
            NotDefineError(f'Var "{statement.name}" not define.').raise_it()
        else:
            val = self.expr(statement.var, ctx, function_ctx)
            # ctx.setitem(statement.name, val)
            return val

    def run_statement(
        self, statement, ctx: CTX, function_ctx: FunctionCTX, catches: list
    ):
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
            return self.expr(statement.val, ctx, function_ctx)  # Return it to the top.
        elif isinstance(statement, Compare):
            return self.expr_compare(
                statement, ctx, function_ctx
            )  # Return the result to the top.
        elif isinstance(statement, IfStatement):
            self.expr_if(statement, ctx, function_ctx)
        elif isinstance(statement, RaiseStatement):
            self.expr_raise_catch(statement, ctx, function_ctx, catches)

        elif isinstance(statement, TryCatch):
            body1 = statement.bodys1
            body2 = statement.bodys2
            errors = statement.catchs

            try:
                self.run_statements(body1, ctx, function_ctx, errors)
            except ErrorException as E:
                self.run_statements(body2, ctx, function_ctx, [])

    def expr_raise_catch(
        self,
        statement: RaiseStatement,
        ctx: CTX,
        function_ctx: FunctionCTX,
        catches: list,
    ):
        if statement.expection in catches:
            raise ErrorException([statement.expection, statement.args])
        self.expr_raise(statement, ctx, function_ctx)

    def expr_compare(self, compare: Compare, ctx: CTX, function_ctx: FunctionCTX):
        return compare.compare(ctx, function_ctx, self.expr)

    def expr_args(self, args, ctx: CTX, function_ctx: FunctionCTX):
        args = list(args)
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
            elif statement.name == "tostr":
                return _tostr(*self.expr_args(statement.args, ctx, function_ctx))
            elif statement.name == "tofloat":
                return _tofloat(*self.expr_args(statement.args, ctx, function_ctx))
        elif function_ctx.is_it_in(statement.name):  # Check the function in the define.
            statement: Call
            function_ctx: list[FunctionDef]

            function_statement = function_ctx[statement.name]
            function_statement: FunctionDef

            temp_ctx = CTX()
            temp_function_ctx = FunctionCTX()

            args = self.expr_args(statement.args, ctx, function_ctx)

            for key, value in zip(
                function_statement.args,
                args,
            ):
                temp_ctx[key] = value

            return self.run_statements(
                function_statement.body, temp_ctx, temp_function_ctx
            )  # Need get value so return it.
        else:
            error_message(f'Function "{statement.name}" not define.')
