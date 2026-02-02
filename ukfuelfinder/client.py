"""
Main client for UK Fuel Finder API.
"""
from typing import List, Optional, Iterator, Any
from .config import Config
from .auth import OAuth2Authenticator
from .http_client import HTTPClient
from .cache import ResponseCache
from .rate_limiter import RateLimiter
from .services.price_service import PriceService
from .services.forecourt_service import ForecourtService
from .models import PFS, PFSInfo, FuelPrice


class FuelFinderClient:
    """
    Client for accessing the UK Government Fuel Finder API.

    Example:
        >>> client = FuelFinderClient(
        ...     client_id="your_client_id",
        ...     client_secret="your_client_secret"
        ... )
        >>> prices = client.get_all_pfs_prices()
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: str = "production",
        cache_enabled: bool = True,
        timeout: int = 30,
    ):
        """
        Initialize Fuel Finder client.

        Args:
            client_id: OAuth client ID (reads from env if not provided)
            client_secret: OAuth client secret (reads from env if not provided)
            environment: "production" or "test"
            cache_enabled: Enable response caching
            timeout: Request timeout in seconds
        """
        if client_id and client_secret:
            self.config = Config(
                client_id=client_id,
                client_secret=client_secret,
                environment=environment,
                timeout=timeout,
                cache_enabled=cache_enabled,
            )
        else:
            self.config = Config.from_env(environment)

        # Initialize components
        self.authenticator = OAuth2Authenticator(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            token_url=self.config.token_url,
            refresh_url=self.config.refresh_url,
        )

        self.rate_limiter = RateLimiter(
            requests_per_minute=self.config.rate_limit_rpm,
            daily_limit=self.config.rate_limit_daily,
        )

        self.http_client = HTTPClient(
            base_url=self.config.base_url,
            authenticator=self.authenticator,
            rate_limiter=self.rate_limiter,
            timeout=self.config.timeout,
        )

        self.cache = ResponseCache() if self.config.cache_enabled else None

        # Initialize services
        self.price_service = PriceService(self.http_client, self.cache or ResponseCache())
        self.forecourt_service = ForecourtService(self.http_client, self.cache or ResponseCache())

    # Price methods
    def get_all_pfs_prices(
        self, batch_number: Optional[int] = None, effective_start_timestamp: Optional[str] = None, **kwargs: Any
    ) -> List[PFS]:
        """
        Get all PFS fuel prices.

        Args:
            batch_number: Batch number for pagination
            effective_start_timestamp: Timestamp in YYYY-MM-DD HH:MM:SS for incremental updates
            **kwargs: Additional parameters

        Returns:
            List of PFS with fuel prices
        """
        return self.price_service.get_all_pfs_prices(
            batch_number=batch_number, effective_start_timestamp=effective_start_timestamp, **kwargs
        )

    def get_pfs(self, node_id: str) -> Optional[PFS]:
        """
        Get specific PFS by node ID.

        Args:
            node_id: Unique PFS identifier

        Returns:
            PFS object or None if not found
        """
        all_pfs = self.get_all_pfs_prices()
        return self.price_service.get_pfs_by_node_id(node_id, all_pfs)

    def get_prices_by_fuel_type(self, fuel_type: str) -> List[FuelPrice]:
        """
        Get all prices for a specific fuel type.

        Args:
            fuel_type: Fuel type (e.g., "unleaded", "diesel")

        Returns:
            List of fuel prices
        """
        all_pfs = self.get_all_pfs_prices()
        return self.price_service.get_prices_by_fuel_type(fuel_type, all_pfs)

    def get_incremental_price_updates(self, since_timestamp: str, **kwargs: Any) -> List[PFS]:
        """
        Get incremental price updates since a specific timestamp.

        Args:
            since_timestamp: Timestamp in YYYY-MM-DD HH:MM:SS format
            **kwargs: Additional parameters

        Returns:
            List of PFS with updated prices
        """
        return self.price_service.get_incremental_updates(since_timestamp, **kwargs)

    # Forecourt methods
    def get_all_pfs_info(
        self, batch_number: Optional[int] = None, **kwargs: Any
    ) -> List[PFSInfo]:
        """
        Get all PFS information.

        Args:
            batch_number: Batch number for pagination (500 per batch)
            **kwargs: Additional parameters

        Returns:
            List of PFS information
        """
        return self.forecourt_service.get_all_pfs(batch_number=batch_number, **kwargs)

    def get_incremental_pfs_info(self, since_timestamp: str, **kwargs: Any) -> List[PFSInfo]:
        """
        Get incremental PFS information updates.

        Args:
            since_timestamp: Timestamp in YYYY-MM-DD HH:MM:SS format
            **kwargs: Additional parameters

        Returns:
            List of updated PFS information
        """
        return self.forecourt_service.get_incremental_pfs(effective_start_timestamp=since_timestamp, **kwargs)

    def get_pfs_info(self, node_id: str) -> Optional[PFSInfo]:
        """
        Get specific PFS information by node ID.

        Args:
            node_id: Unique PFS identifier

        Returns:
            PFSInfo object or None if not found
        """
        all_pfs = self.get_all_pfs_info()
        return self.forecourt_service.get_pfs_by_node_id(node_id, all_pfs)

    def get_all_pfs_paginated(self) -> Iterator[List[PFSInfo]]:
        """
        Get all PFS information with automatic pagination.

        Yields:
            Lists of PFS information (up to 500 per batch)
        """
        return self.forecourt_service.get_all_pfs_paginated()

    # Utility methods
    def clear_cache(self) -> None:
        """Clear all cached responses."""
        if self.cache:
            self.cache.clear()

    def set_cache_ttl(self, resource_type: str, ttl: int) -> None:
        """
        Set cache TTL for a resource type.

        Args:
            resource_type: "prices" or "forecourts"
            ttl: Time to live in seconds
        """
        if resource_type == "prices":
            self.price_service.cache_ttl = ttl
        elif resource_type == "forecourts":
            self.forecourt_service.cache_ttl = ttl

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        if self.cache:
            return self.cache.get_stats()
        return {}
