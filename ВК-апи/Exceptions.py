class ExceptionsFactory:
    def get_exceptions(self):
        return (
            InvalidIdException,
            KeyboardInterrupt,
            NoFriendsException,
            PrivateAccountException,
            NoAlbumsException,
            NoGroupsException,
            UnicodeEncodeError
        )


class InvalidIdException(Exception):
    def __init__(self, message="Wrong id"):
        super().__init__(message)


class NoFriendsException(Exception):
    def __init__(self, message="User has no friends :("):
        super().__init__(message)


class PrivateAccountException(Exception):
    def __init__(self, message="User account is private"):
        super().__init__(message)


class NoAlbumsException(Exception):
    def __init__(self, message="User has no albums"):
        super().__init__(message)


class NoGroupsException(Exception):
    def __init__(self, message="User has no albums"):
        super().__init__(message)
