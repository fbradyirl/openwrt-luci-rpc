
class InvalidLuciLoginError(Exception):
    """When an invalid login is detected."""

    def __init__(self, message):
        self.message = message

    pass


class PageNotFoundError(Exception):
    """When a 404 happens."""

    def __init__(self, message):
        self.message = message

    pass


class InvalidLuciTokenError(Exception):
    """When an invalid token is detected."""

    pass


class LuciRpcMethodNotFoundError(Exception):
    """When an invalid method is called."""

    pass


class LuciRpcUnknownError(Exception):
    """When a general unknown exception happens."""

    pass
