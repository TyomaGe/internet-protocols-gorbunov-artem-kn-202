class InvalidIpAddress(Exception):
    def __init__(self, message="Wrong ip address"):
        super().__init__(message)


class InvalidProtocol(Exception):
    def __init__(self, message="Invalid protocol"):
        super().__init__(message)


class InvalidPortRange(Exception):
    def __init__(self, message="Invalid port range"):
        super().__init__(message)


exceptions = (
    InvalidProtocol,
    InvalidIpAddress,
    InvalidPortRange,
    ValueError,
    TypeError
)
