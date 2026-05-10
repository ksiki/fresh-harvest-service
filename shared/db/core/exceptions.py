class SubscriptionNotFoundError(Exception):
    def __init__(self, message="Free subscription record is missing in the database"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExists(Exception):
    def __init__(self, message="User already exists in the database"):
        self.message = message
        super().__init__(self.message)


class UserNotExists(Exception):
    def __init__(self, message="User not exists in the database"):
        self.message = message
        super().__init__(self.message)
