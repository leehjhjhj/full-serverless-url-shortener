class NotFoundException(Exception):
    def __init__(self, message="Url not found"):
        self.message = message
        super().__init__(self.message)

class ForbiddenException(Exception):
    def __init__(self, message="Forbidden"):
        self.message = message
        super().__init__(self.message)

class AlreadyExistException(Exception):
    def __init__(self, message="Url already existed"):
        self.message = message
        super().__init__(self.message)


class TooLongExceiption(Exception):
    def __init__(self, message="Hopong hash too long"):
        self.message = message
        super().__init__(self.message)
