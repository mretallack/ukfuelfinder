"""
OAuth 2.0 authentication for UK Fuel Finder API.
"""

import time
import threading
from typing import Optional
import requests
from .exceptions import AuthenticationError, InvalidCredentialsError


class OAuth2Authenticator:
    """Manages OAuth 2.0 authentication and token lifecycle."""

    def __init__(self, client_id: str, client_secret: str, token_url: str, refresh_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.refresh_url = refresh_url
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expiry: float = 0
        self._lock = threading.Lock()

    def get_token(self) -> str:
        """Get valid access token, refreshing if necessary."""
        with self._lock:
            if self._is_token_valid():
                return self._access_token  # type: ignore

            # Try refresh token first if available
            if self._refresh_token:
                try:
                    return self._refresh_access_token()
                except AuthenticationError:
                    # Fall back to generating new token
                    pass

            return self._generate_token()

    def _is_token_valid(self) -> bool:
        """Check if current token is valid and not expiring soon."""
        if not self._access_token:
            return False
        # Refresh 60 seconds before expiry
        return time.time() < (self._token_expiry - 60)

    def _generate_token(self) -> str:
        """Generate new access token using client credentials."""
        try:
            response = requests.post(
                self.token_url,
                json={"client_id": self.client_id, "client_secret": self.client_secret},
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if response.status_code == 401:
                raise InvalidCredentialsError("Invalid client credentials")

            response.raise_for_status()
            data = response.json()

            # Handle nested response structure
            if "data" in data:
                token_data = data["data"]
            else:
                token_data = data

            self._access_token = token_data["access_token"]
            self._refresh_token = token_data.get("refresh_token")
            self._token_expiry = time.time() + token_data["expires_in"]

            return self._access_token

        except requests.RequestException as e:
            raise AuthenticationError(f"Failed to generate access token: {e}")

    def _refresh_access_token(self) -> str:
        """Refresh access token using refresh token."""
        if not self._refresh_token:
            raise AuthenticationError("No refresh token available")

        try:
            response = requests.post(
                self.refresh_url,
                json={"client_id": self.client_id, "refresh_token": self._refresh_token},
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if response.status_code in (400, 401):
                raise AuthenticationError("Refresh token expired or invalid")

            response.raise_for_status()
            data = response.json()

            # Handle nested response structure
            if "data" in data:
                token_data = data["data"]
            else:
                token_data = data

            self._access_token = token_data["access_token"]
            self._refresh_token = token_data.get("refresh_token", self._refresh_token)
            self._token_expiry = time.time() + token_data["expires_in"]

            return self._access_token

        except requests.RequestException as e:
            raise AuthenticationError(f"Failed to refresh access token: {e}")
