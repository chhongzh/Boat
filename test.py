from define_statement import (
    BinOp,
    Call,
    FunctionDef,
    Module,
    ReturnStatement,
    Var,
    VarAssignment,
    VarDef,
    Compare,
    WhileStatement,
)
from define_type import NE, PLUS, ObjInt, ObjStr, EQ, ObjFloat, SUBTRACT, GT, LE


# Example "Hello World!"
CODE = Module([Call("print", ["Hello World"])])
