"""
Configuration management for UK Fuel Finder API client.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration for Fuel Finder API client."""

    client_id: str
    client_secret: str
    environment: str = "production"
    timeout: int = 30
    cache_enabled: bool = True
    rate_limit_rpm: int = 120
    rate_limit_daily: int = 10000

    @property
    def base_url(self) -> str:
        """Get base URL for the environment."""
        if self.environment == "test":
            return "https://test.fuel-finder.service.gov.uk/api/v1"
        return "https://www.fuel-finder.service.gov.uk/api/v1"

    @property
    def token_url(self) -> str:
        """Get token URL for the environment."""
        return f"{self.base_url}/oauth/generate_access_token"

    @property
    def refresh_url(self) -> str:
        """Get refresh token URL for the environment."""
        return f"{self.base_url}/oauth/regenerate_access_token"

    @classmethod
    def from_env(cls, environment: Optional[str] = None) -> "Config":
        """Create configuration from environment variables."""
        client_id = os.getenv("FUEL_FINDER_CLIENT_ID")
        client_secret = os.getenv("FUEL_FINDER_CLIENT_SECRET")
        env = environment or os.getenv("FUEL_FINDER_ENVIRONMENT", "production")

        if not client_id or not client_secret:
            raise ValueError(
                "FUEL_FINDER_CLIENT_ID and FUEL_FINDER_CLIENT_SECRET "
                "environment variables must be set"
            )

        # Adjust rate limits for test environment
        rate_limit_rpm = 30 if env == "test" else 120
        rate_limit_daily = 5000 if env == "test" else 10000

        return cls(
            client_id=client_id,
            client_secret=client_secret,
            environment=env,
            rate_limit_rpm=rate_limit_rpm,
            rate_limit_daily=rate_limit_daily,
        )
