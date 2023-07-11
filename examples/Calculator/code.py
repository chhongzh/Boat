from boat.statement import *
from boat.type import *

CODE = Module(
    [
        FunctionDef(
            "plus",
            ["a", "b"],
            [ObjInt, ObjInt],
            [ReturnStatement(BinOp(Var("a"), Var("b"), PLUS))],
        ),
        FunctionDef(
            "subtract",
            ["a", "b"],
            [ObjInt, ObjInt],
            [ReturnStatement(BinOp(Var("a"), Var("b"), SUBTRACT))],
        ),
        FunctionDef(
            "multiply",
            ["a", "b"],
            [ObjInt, ObjInt],
            [ReturnStatement(BinOp(Var("a"), Var("b"), MULTIPLY))],
        ),
        FunctionDef(
            "divide",
            ["a", "b"],
            [ObjInt, ObjInt],
            [ReturnStatement(BinOp(Var("a"), Var("b"), DIVIDE))],
        ),
        VarDef("in", ObjStr),
        VarDef("a", ObjInt),
        VarDef("b", ObjInt),
        Call(
            "print",
            [
                "Calculator",
                "\n",
                "Type 1 for plus.",
                "\n",
                "Type 2 for subtract.",
                "\n",
                "Type 3 for multiply.",
                "\n",
                "Type 4 for divide.",
            ],
        ),
        VarDef("result", ObjFloat),
        VarAssignment("in", Call("input", ["Choice:"])),
        VarAssignment("a", Call("toint", [Call("input", ["Num a:"])])),
        VarAssignment("b", Call("toint", [Call("input", ["Num b:"])])),
        IfStatement(
            [
                Compare(Var("in"), "1", EQ),
                Compare(Var("in"), "2", EQ),
                Compare(Var("in"), "3", EQ),
                Compare(Var("in"), "4", EQ),
            ],
            [
                [VarAssignment("result", Call("plus", [Var("a"), Var("b")]))],
                [VarAssignment("result", Call("subtract", [Var("a"), Var("b")]))],
                [VarAssignment("result", Call("multiply", [Var("a"), Var("b")]))],
                [VarAssignment("result", Call("divide", [Var("a"), Var("b")]))],
                [Call("print", ["Invalid number!"])],
            ],
        ),
        Call("print", ["Result:", Var("result")]),
    ]
)
