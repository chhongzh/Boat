from boat.statement import (
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
    IfStatement,
)
from boat.type import (
    NE,
    PLUS,
    ObjInt,
    ObjStr,
    EQ,
    ObjFloat,
    SUBTRACT,
    GT,
    LE,
    MULTIPLY,
    DIVIDE,
)


# Example "Hello World!"
CODE = Module([Call("print", ["Running on Boat AST!"])])
