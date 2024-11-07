class NotFoundException(Exception):
    def __init__(self, message="Url not found"):
        self.message = message
        super().__init__(self.message)

class ForbiddenException(Exception):
    def __init__(self, message="Forbidden"):
        self.message = message
        super().__init__(self.message)