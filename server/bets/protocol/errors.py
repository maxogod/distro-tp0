
class InconsistentBatchSizeError(Exception):
    def __init__(self, size_expected: int):
        """ Raised when the number of bets received does not match the expected batch size. """
        self.size_expected = size_expected

    def __str__(self):
        return f"InconsistentBatchSizeError({self.size_expected})"

class ConnectionClosedError(Exception):
    def __init__(self, message: str):
        """ Raised when the socket connection is closed unexpectedly. """
        self.message = message

    def __str__(self):
        return f"ConnectionClosedError({self.message})"

class AgencyIDNotSetError(Exception):
    def __init__(self, message: str):
        """ Raised when the agency ID has not been set before sending bets. """
        self.message = message

    def __str__(self):
        return f"AgencyIDNotSetError({self.message})"
