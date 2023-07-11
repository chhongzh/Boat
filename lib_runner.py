from typing import Any

# from define_statement import FunctionDef


class CTX(object):
    def __init__(self):
        self.__data = {}

    def __setitem__(self, __name: str, __value: Any) -> None:
        self.__data[__name] = __value

    def setitem(self, name, val):
        self.__data[name] = val

    def __getitem__(self, __name: str) -> Any:
        return self.__data[__name]

    def is_it_in(self, name: str):
        return name in self.__data

    def __repr__(self):
        return str(self.__data)


class FunctionCTX(object):
    def __init__(self):
        self.__data = {}

    def __getitem__(self, name):
        return self.__data[name]

    def new_function(self, obj):
        self.__data[obj.name] = obj

    def is_it_in(self, name: str):
        return name in self.__data


def error_message(*msg: str, sep=" "):
    print(f"ERR:{sep.join(map(str,msg))}")
    exit(1)


def debug_message(*msg: str, sep=" "):
    print(f"[DEBUG]:{sep.join(map(str,msg))}")
