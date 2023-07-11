import copy
from define_type import *
from lib_runner import CTX, FunctionCTX, debug_message


class Module(object):
    def __init__(self, body: list):
        self.body = body


class FunctionDef(object):
    def __init__(self, name: str, args: list, args_type: list, body: list):
        self.name = name
        self.args_type = args_type
        self.args = args
        self.body = body


class VarDef(object):
    def __init__(self, name: str, type: ObjFloat | ObjInt | ObjStr):
        self.name = name
        self.type = type


class VarAssignment(object):
    def __init__(self, name: str, val):
        self.name = name
        self.var = val


class Var(object):
    def __init__(self, var: str):
        self.var = var


class IfStatement(object):
    def __init__(self, tests: list, bodys: list):
        self.tests = tests
        self.bodys = bodys


class Compare(object):
    def __init__(self, a, b, op):
        self.a = a
        self.b = b
        self.op = op

    def compare(self, ctx: CTX, function_ctx: FunctionCTX, expr_method):
        # if isinstance(self.a, Compare):
        #     self.a.compare()
        # elif isinstance(self.b, Compare):
        #     self.b.compare()
        a, b = copy.deepcopy(self.a), copy.deepcopy(self.b)
        a = expr_method(a, ctx, function_ctx)
        b = expr_method(b, ctx, function_ctx)

        if self.op == EQ:
            return a == b
        elif self.op == NE:
            return a != b
        elif self.op == LT:
            return a < b
        elif self.op == LE:
            return a <= b
        elif self.op == GE:
            return a >= b
        elif self.op == GT:
            return a > b


class Call(object):
    def __init__(self, name: str, args: list):
        self.name = name
        self.args = args


class ReturnStatement(object):
    def __init__(self, val):
        self.val = val


class WhileStatement(object):
    def __init__(self, test: Compare, body: list):
        self.test = test
        self.body = body


class BinOp(object):
    def __init__(self, left, right, op: list[int]):
        self.left = left
        self.right = right
        self.op = op

    def calc(self, ctx: CTX, function_ctx: FunctionCTX, expr_method):
        left = copy.deepcopy(self.left)
        right = copy.deepcopy(self.right)
        if isinstance(self.left, BinOp):
            left = self.left.calc()
        if isinstance(self.right, BinOp):
            right = self.right.calc()

        debug_message("BinOp计算", "Left", left, "Right", right)

        left = expr_method(left, ctx, function_ctx)
        right = expr_method(right, ctx, function_ctx)

        if self.op == PLUS:
            return left + right
        elif self.op == SUBTRACT:
            return left - right
        elif self.op == MULTIPLY:
            return left * right
        elif self.op == DIVIDE:
            return left / right
