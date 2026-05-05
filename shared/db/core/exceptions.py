class SubscriptionNotFoundError(Exception):
    def __init__(self, message="Free subscription record is missing in the database"):
        self.message = message
        super().__init__(self.message)
