"""
Exceptions for the UK Fuel Finder API client.
"""


class FuelFinderError(Exception):
    """Base exception for all Fuel Finder errors."""

    pass


class AuthenticationError(FuelFinderError):
    """Raised when authentication fails."""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when client credentials are invalid."""

    pass


class TokenExpiredError(AuthenticationError):
    """Raised when access token has expired."""

    pass


class APIError(FuelFinderError):
    """Base exception for API-related errors."""

    pass


class NotFoundError(APIError):
    """Raised when requested resource is not found (404)."""

    pass


class BatchNotFoundError(NotFoundError):
    """Raised when a batch number is not found (404)."""

    pass


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded (429)."""

    def __init__(self, message: str, retry_after: int = 0) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class ServerError(APIError):
    """Raised when API returns a server error (5xx)."""

    pass


class ValidationError(APIError):
    """Raised when request validation fails (400)."""

    pass


class InvalidBatchNumberError(ValidationError):
    """Raised when a batch number is invalid (backward compatibility)."""

    pass


class NetworkError(FuelFinderError):
    """Base exception for network-related errors."""

    pass


class TimeoutError(NetworkError):
    """Raised when a request times out."""

    pass


class ConnectionError(NetworkError):
    """Raised when connection to API fails."""

    pass


class ResponseParseError(FuelFinderError):
    """Raised when API response cannot be parsed."""

    pass
