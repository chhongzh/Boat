from boat.statement import *
from boat.type import *

CODE = Module(
    [
        Call(
            "print",
            ["This example will show you what to do when Boat AST encounters an error"],
        ),
        Call("input", "To continue, press enter."),
        TryCatch(
            [RaiseStatement("Error", [])], ["Error"], [Call("print", ["Catch error!"])]
        ),
    ]
)
