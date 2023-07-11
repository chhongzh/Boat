def _print(*args):
    # args[Any]

    print("".join(map(str, args)))


def _input(*args):
    return input("".join(map(str, args)))
