"""
HTTP client for UK Fuel Finder API.
"""

import logging
from typing import Any, Dict, Optional

import requests

from .auth import OAuth2Authenticator
from .exceptions import BatchNotFoundError
from .exceptions import ConnectionError as FuelFinderConnectionError
from .exceptions import (NotFoundError, RateLimitError, ResponseParseError,
                         ServerError)
from .exceptions import TimeoutError as FuelFinderTimeoutError
from .exceptions import ValidationError
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class HTTPClient:
    """HTTP client with authentication and error handling."""

    def __init__(
        self,
        base_url: str,
        authenticator: OAuth2Authenticator,
        rate_limiter: RateLimiter,
        timeout: int = 30,
    ):
        self.base_url = base_url
        self.authenticator = authenticator
        self.rate_limiter = rate_limiter
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make GET request to API."""
        return self._make_request("GET", endpoint, params=params)

    def _make_request(
        self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, retries: int = 3
    ) -> Any:
        """Make HTTP request with retries and error handling."""
        url = f"{self.base_url}{endpoint}"

        for attempt in range(retries):
            try:
                # Acquire rate limit permission
                self.rate_limiter.acquire()

                # Get valid token
                token = self.authenticator.get_token()

                # Make request
                headers = {"Authorization": f"Bearer {token}"}
                logger.debug(f"{method} {url} params={params}")

                response = self.session.request(
                    method, url, headers=headers, params=params, timeout=self.timeout
                )

                return self._handle_response(response)

            except RateLimitError as e:
                if attempt < retries - 1:
                    self.rate_limiter.handle_rate_limit_error(e.retry_after)
                    continue
                raise

            except requests.Timeout:
                if attempt < retries - 1:
                    continue
                raise FuelFinderTimeoutError(f"Request to {url} timed out")

            except requests.ConnectionError as e:
                if attempt < retries - 1:
                    continue
                raise FuelFinderConnectionError(f"Connection to {url} failed: {e}")

        raise ServerError("Max retries exceeded")

    def _handle_response(self, response: requests.Response) -> Any:
        """Handle HTTP response and errors."""
        logger.debug(f"Response: {response.status_code} in {response.elapsed.total_seconds():.2f}s")

        if response.status_code == 200:
            try:
                data = response.json()
                # Handle nested response structure with "data" wrapper
                if isinstance(data, dict) and "data" in data:
                    return data["data"]
                # Handle old response format with success/message fields
                if isinstance(data, dict) and "success" in data:
                    # Old format: extract data from wrapper
                    return data.get("data", data)
                return data
            except ValueError as e:
                raise ResponseParseError(f"Failed to parse JSON response: {e}")

        elif response.status_code == 400:
            raise ValidationError(f"Invalid request: {response.text}")

        elif response.status_code == 401:
            raise ValidationError("Unauthorized - token may be invalid")

        elif response.status_code == 404:
            # Check if this is a batch-related endpoint
            if "/fuel-prices/" in response.url or "/pfs/" in response.url:
                raise BatchNotFoundError(f"Batch not found: {response.url}")
            raise NotFoundError(f"Resource not found: {response.url}")

        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 0))
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)

        elif response.status_code >= 500:
            raise ServerError(f"Server error: {response.status_code} - {response.text}")

        else:
            raise ServerError(f"Unexpected status code: {response.status_code}")
