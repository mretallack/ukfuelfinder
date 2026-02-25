"""
UK Fuel Finder Python Library

Python library for accessing the UK Government Fuel Finder API.
"""

__version__ = "3.0.0"

from .client import FuelFinderClient
from .config import set_global_backward_compatible
from .exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    FuelFinderError,
    InvalidCredentialsError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ResponseParseError,
    ServerError,
    TimeoutError,
    TokenExpiredError,
    ValidationError,
)
from .models import PFS, Address, FuelPrice, Location, PFSInfo

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
    "set_global_backward_compatible",
]
