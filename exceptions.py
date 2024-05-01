"""
exceptions
~~~~~~~~~~
This module contains exceptions that are thrown by the ReservationApi
when the API responds with a non-200 or 5xx error
"""

from requests.exceptions import RequestException

# 400 error
class BadRequestError(RequestException):
    """A 400 Bad Request error occurred."""

# 401 error
class InvalidTokenError(RequestException):
    """The API token was invalid or missing."""

# 403 error
class BadSlotError(RequestException):
    """The requested slot does not exist."""

# 404 error
class NotProcessedError(RequestException):
    """The request has not been processed."""

# 409 error
class SlotUnavailableError(RequestException):
    """The requested slot is not available."""

# 451 error
class ReservationLimitError(RequestException):
    """The client already holds the maximum number of reservations."""

# Maximum Number of Tries
class MaxRetriesExhaustedError(Exception):
    """Exception raised when maximum retries are exhausted"""
    def __init__(self, message="Maximum retries exhausted"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
