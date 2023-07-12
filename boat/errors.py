from .lib_runner import error_message


class BaseError(object):
    def __init__(self, *args):
        self.args = args

    def raise_it(self):
        error_message(
            f"{type(self).__name__}:{self.args[0] if len(self.args)==1 else self.args}"
        )


class Error(BaseError):
    pass


class SystemError(BaseError):
    pass


class RunError(SystemError):
    pass


class ExpressError(SystemError):
    pass


ERRORS_MAP = {
    "BaseError": BaseError,
    "SystemError": SystemError,
    "Error": Error,
    "RunError": RunError,
    "ExpressError": ExpressError,
}

if __name__ == "__main__":
    E = Error("s")

    E.raise_it()
