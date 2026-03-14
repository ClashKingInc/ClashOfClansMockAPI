class ClientError(Exception):
    def __init__(self, reason: str, message: str, status: int):
        self.reason = reason
        self.message = message
        self.status = status
