"""
Main client for UK Fuel Finder API.
"""

import os
from math import asin, cos, radians, sin, sqrt
from typing import Any, Iterator, List, Optional, Tuple, Union

from .auth import OAuth2Authenticator
from .cache import ResponseCache
from .compatibility import BackwardCompatibleResponse
from .config import Config, get_global_backward_compatible
from .exceptions import BatchNotFoundError, InvalidBatchNumberError
from .http_client import HTTPClient
from .models import PFS, FuelPrice, PFSInfo
from .rate_limiter import RateLimiter
from .services.forecourt_service import ForecourtService
from .services.price_service import PriceService


class FuelFinderClient:
    """
    Client for accessing the UK Government Fuel Finder API.

    Example:
        >>> client = FuelFinderClient(
        ...     client_id="your_client_id",
        ...     client_secret="your_client_secret"
        ... )
        >>> prices = client.get_all_pfs_prices()

    Backward Compatibility:
        >>> # With backward compatibility (default)
        >>> client = FuelFinderClient(backward_compatible=True)
        >>> prices = client.get_all_pfs_prices()
        >>> print(prices[0].success)  # Returns True
        >>> print(prices[0].message)  # Returns empty string

        >>> # Without backward compatibility
        >>> client = FuelFinderClient(backward_compatible=False)
        >>> prices = client.get_all_pfs_prices()
        >>> # prices[0].success and prices[0].message not available
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: str = "production",
        cache_enabled: bool = True,
        timeout: int = 30,
        backward_compatible: bool = True,
    ):
        """
        Initialize Fuel Finder client.

        Args:
            client_id: OAuth client ID (reads from env if not provided)
            client_secret: OAuth client secret (reads from env if not provided)
            environment: "production" or "test"
            cache_enabled: Enable response caching
            timeout: Request timeout in seconds
            backward_compatible: Enable backward compatibility mode for API changes
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

        # Priority: global config > env var > parameter
        global_config = get_global_backward_compatible()
        env_backward_compatible = os.getenv("UKFUELFINDER_BACKWARD_COMPATIBLE")

        if global_config is not None:
            self.backward_compatible = global_config
        elif env_backward_compatible is not None:
            self.backward_compatible = env_backward_compatible.lower() in ("1", "true", "yes")
        else:
            self.backward_compatible = backward_compatible

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
        self,
        batch_number: Optional[int] = None,
        effective_start_timestamp: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[List[PFS], List[BackwardCompatibleResponse[PFS]]]:
        """
        Get all PFS fuel prices.

        Args:
            batch_number: Batch number for pagination (500 per batch).
                         If None, automatically fetches all batches.
            effective_start_timestamp: Timestamp in YYYY-MM-DD HH:MM:SS for incremental updates
            **kwargs: Additional parameters

        Returns:
            List of PFS with fuel prices
        """
        try:
            if batch_number is not None:
                # Fetch specific batch
                pfs_list = self.price_service.get_all_pfs_prices(
                    batch_number=batch_number,
                    effective_start_timestamp=effective_start_timestamp,
                    **kwargs,
                )
            else:
                # Fetch all batches automatically
                pfs_list = self.price_service.get_all_pfs_prices_paginated(
                    effective_start_timestamp=effective_start_timestamp, **kwargs
                )
        except BatchNotFoundError as e:
            # Handle backward compatibility for batch errors
            if self.backward_compatible:
                raise InvalidBatchNumberError(f"Invalid batch number: {batch_number}") from e
            raise

        # Apply backward compatibility wrapper if enabled
        if self.backward_compatible:
            return [BackwardCompatibleResponse(pfs) for pfs in pfs_list]
        return pfs_list

    def get_pfs(self, node_id: str) -> Optional[Union[PFS, BackwardCompatibleResponse[PFS]]]:
        """
        Get specific PFS by node ID.

        Args:
            node_id: Unique PFS identifier

        Returns:
            PFS object or None if not found
        """
        all_pfs = self.get_all_pfs_prices()
        pfs = self.price_service.get_pfs_by_node_id(node_id, all_pfs)

        # Apply backward compatibility wrapper if enabled
        if pfs and self.backward_compatible:
            return BackwardCompatibleResponse(pfs)
        return pfs

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

    def get_incremental_price_updates(
        self, since_timestamp: str, **kwargs: Any
    ) -> Union[List[PFS], List[BackwardCompatibleResponse[PFS]]]:
        """
        Get incremental price updates since a specific timestamp.

        Args:
            since_timestamp: Timestamp in YYYY-MM-DD HH:MM:SS format
            **kwargs: Additional parameters

        Returns:
            List of PFS with updated prices
        """
        pfs_list = self.price_service.get_incremental_updates(since_timestamp, **kwargs)

        # Apply backward compatibility wrapper if enabled
        if self.backward_compatible:
            return [BackwardCompatibleResponse(pfs) for pfs in pfs_list]
        return pfs_list

    # Forecourt methods
    def get_all_pfs_info(
        self, batch_number: Optional[int] = None, **kwargs: Any
    ) -> Union[List[PFSInfo], List[BackwardCompatibleResponse[PFSInfo]]]:
        """
        Get all PFS information.

        Args:
            batch_number: Batch number for pagination (500 per batch).
                         If None, automatically fetches all batches.
            **kwargs: Additional parameters

        Returns:
            List of PFS information
        """
        try:
            if batch_number is not None:
                # Fetch specific batch
                pfs_list = self.forecourt_service.get_all_pfs(batch_number=batch_number, **kwargs)
            else:
                # Fetch all batches automatically
                all_pfs = []
                for batch in self.forecourt_service.get_all_pfs_paginated(**kwargs):
                    all_pfs.extend(batch)
                pfs_list = all_pfs
        except BatchNotFoundError as e:
            # Handle backward compatibility for batch errors
            if self.backward_compatible:
                raise InvalidBatchNumberError(f"Invalid batch number: {batch_number}") from e
            raise

        # Apply backward compatibility wrapper if enabled
        if self.backward_compatible:
            return [BackwardCompatibleResponse(pfs) for pfs in pfs_list]
        return pfs_list

    def get_incremental_pfs_info(
        self, since_timestamp: str, **kwargs: Any
    ) -> Union[List[PFSInfo], List[BackwardCompatibleResponse[PFSInfo]]]:
        """
        Get incremental PFS information updates.

        Args:
            since_timestamp: Timestamp in YYYY-MM-DD HH:MM:SS format
            **kwargs: Additional parameters

        Returns:
            List of updated PFS information
        """
        pfs_list = self.forecourt_service.get_incremental_pfs(
            effective_start_timestamp=since_timestamp, **kwargs
        )

        # Apply backward compatibility wrapper if enabled
        if self.backward_compatible:
            return [BackwardCompatibleResponse(pfs) for pfs in pfs_list]
        return pfs_list

    def get_pfs_info(
        self, node_id: str
    ) -> Optional[Union[PFSInfo, BackwardCompatibleResponse[PFSInfo]]]:
        """
        Get specific PFS information by node ID.

        Args:
            node_id: Unique PFS identifier

        Returns:
            PFSInfo object or None if not found
        """
        all_pfs = self.get_all_pfs_info()
        pfs = self.forecourt_service.get_pfs_by_node_id(node_id, all_pfs)

        # Apply backward compatibility wrapper if enabled
        if pfs and self.backward_compatible:
            return BackwardCompatibleResponse(pfs)
        return pfs

    def get_all_pfs_paginated(
        self,
    ) -> Iterator[Union[List[PFSInfo], List[BackwardCompatibleResponse[PFSInfo]]]]:
        """
        Get all PFS information with automatic pagination.

        Yields:
            Lists of PFS information (up to 500 per batch)
        """
        for batch in self.forecourt_service.get_all_pfs_paginated():
            # Apply backward compatibility wrapper if enabled
            if self.backward_compatible:
                yield [BackwardCompatibleResponse(pfs) for pfs in batch]
            else:
                yield batch

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

    def search_by_location(
        self, latitude: float, longitude: float, radius_km: float = 5.0
    ) -> List[Tuple[float, Union[PFSInfo, BackwardCompatibleResponse[PFSInfo]]]]:
        """
        Search for fuel stations near a location.

        Args:
            latitude: Search center latitude
            longitude: Search center longitude
            radius_km: Search radius in kilometers (default: 5.0)

        Returns:
            List of tuples (distance_km, PFSInfo) sorted by distance
        """
        sites = self.get_all_pfs_info()
        nearby = []

        for site in sites:
            # Unwrap if it's a BackwardCompatibleResponse for distance calculation
            actual_site = site._response if hasattr(site, "_response") else site

            if (
                actual_site.location
                and actual_site.location.latitude
                and actual_site.location.longitude
            ):
                distance = self._haversine(
                    longitude,
                    latitude,
                    actual_site.location.longitude,
                    actual_site.location.latitude,
                )
                if distance <= radius_km:
                    nearby.append((distance, site))

        nearby.sort(key=lambda x: x[0])
        return nearby

    @staticmethod
    def _haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """Calculate distance between two points in kilometers using Haversine formula."""
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        return 6371 * c
