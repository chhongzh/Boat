from boat.lib_runner import error_message


def _print(*args):
    # args[Any]

    print("".join(map(str, args)))


def _input(*args):
    return input("".join(map(str, args)))


def _toint(a: str):
    try:
        return int(a)
    except TypeError:
        error_message("Invalid number.")


def _tostr(a):
    return str(a)


def _tofloat(a):
    try:
        return float(a)
    except:
        error_message("Invalid number.")
