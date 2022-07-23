class NotFoundRequest(Exception):

    def __init__(self, fn_name: str):
        self.fn_name = fn_name

    def __str__(self):
        return (
            f'In "{self.fn_name}" view, "Request object" was not detected in the argument.',
            'If you run into any issues, please report them here: (https://github.com/iml1111/django-jwt-extended/issues)'
        )


class NotFoundSecretKey(Exception):
    def __str__(self):
        return f'In Settings, "SECRET_KEY" was not detected.'


class ConfigIsNotDict(Exception):
    def __str__(self):
        return '"JWT_EXTENDED" config must be "dict" type.'


class InvalidJwtAlgorithm(Exception):

    def __init__(self, param: str, algorithms):
        self.param = param
        self.algorithms = algorithms

    def __str__(self):
        return (
            f'Invalid JWT Algorithm "{self.param}". '
            f'ALGORITHM must be in {self.algorithms}.'
        )


class InvalidLocation(Exception):

    def __init__(self, param: str, locations):
        self.param = param
        self.locations = locations

    def __str__(self):
        return (
            f'Invalid Location "{self.param}". '
            f'LOCATION must be "list", in {self.locations}.'
        )


class InvalidExpires(Exception):

    def __init__(self, target: str):
        self.target = target

    def __str__(self):
        return (
            f'Invalid {self.target} Expires. '
            f'EXPIRES must be a "timedelta" or "int"(value > 0)'
        )


class InvalidRequest(Exception):

    def __init__(self, param: str):
        self.param = param

    def __str__(self):
        return (
            f"Missing Django Request Object."
            f", not {self.param}"
        )


class InvalidOptional(Exception):

    def __init__(self, param: str):
        self.param = param

    def __str__(self):
        return (
            f"'optional' param must be bool type, not {self.param}."
        )


class InvalidRefresh(Exception):

    def __init__(self, param: str):
        self.param = param

    def __str__(self):
        return (
            f"'refresh' param must be bool type, not {self.param}."
        )


class InvalidJsonFormat(Exception):

    def __str__(self):
        return (
            f"Invalid JSON format."
            f"Error config must be JSON serializable."
        )