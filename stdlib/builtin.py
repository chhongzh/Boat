from boat.lib_runner import error_message


def _print(*args):
    # args[Any]

    print("".join(map(str, args)))


def _input(*args):
    return input("".join(map(str, args)))


def _toint(a: str):
    if not a.isdigit():
        error_message("Invalid number.")
    return int(a)
