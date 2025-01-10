
class ClientError(Exception):
	def __init__(self, reason, message, status):
		self.reason: str = reason
		self.message: str = message
		self.status: int = status