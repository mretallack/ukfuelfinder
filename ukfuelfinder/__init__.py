"""
UK Fuel Finder Python Library

Python library for accessing the UK Government Fuel Finder API.
"""

__version__ = "1.2.0"

from .client import FuelFinderClient
from .exceptions import (
    FuelFinderError,
    AuthenticationError,
    InvalidCredentialsError,
    TokenExpiredError,
    APIError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    NetworkError,
    TimeoutError,
    ConnectionError,
    ResponseParseError,
)
from .models import PFS, PFSInfo, FuelPrice, Address, Location

__all__ = [
    "FuelFinderClient",
    "FuelFinderError",
    "AuthenticationError",
    "InvalidCredentialsError",
    "TokenExpiredError",
    "APIError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    "NetworkError",
    "TimeoutError",
    "ConnectionError",
    "ResponseParseError",
    "PFS",
    "PFSInfo",
    "FuelPrice",
    "Address",
    "Location",
]
