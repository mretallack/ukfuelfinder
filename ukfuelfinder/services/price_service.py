"""
Price service for UK Fuel Finder API.
"""

from typing import List, Optional, Dict, Any
from ..http_client import HTTPClient
from ..cache import ResponseCache
from ..models import PFS, FuelPrice


class PriceService:
    """Service for fuel price operations."""

    def __init__(self, http_client: HTTPClient, cache: ResponseCache):
        self.http_client = http_client
        self.cache = cache
        self.cache_ttl = 900  # 15 minutes for prices

    def get_all_pfs_prices(
        self,
        batch_number: Optional[int] = None,
        effective_start_timestamp: Optional[str] = None,
        use_cache: bool = True,
    ) -> List[PFS]:
        """
        Get all PFS fuel prices.

        Args:
            batch_number: Batch number for pagination
            effective_start_timestamp: Timestamp in YYYY-MM-DD HH:MM:SS format for incremental updates
            use_cache: Whether to use cached response

        Returns:
            List of PFS with fuel prices
        """
        params: Dict[str, Any] = {}
        if batch_number:
            params["batch-number"] = batch_number
        if effective_start_timestamp:
            params["effective-start-timestamp"] = effective_start_timestamp

        cache_key = self.cache.generate_key("/pfs/fuel-prices", params)

        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return [PFS.from_dict(item) for item in cached]

        response = self.http_client.get("/pfs/fuel-prices", params=params)
        self.cache.set(cache_key, response, self.cache_ttl)

        return [PFS.from_dict(item) for item in response]

    def get_pfs_by_node_id(self, node_id: str, pfs_list: List[PFS]) -> Optional[PFS]:
        """Get specific PFS by node ID from a list."""
        for pfs in pfs_list:
            if pfs.node_id == node_id:
                return pfs
        return None

    def get_prices_by_fuel_type(self, fuel_type: str, pfs_list: List[PFS]) -> List[FuelPrice]:
        """Get all prices for a specific fuel type."""
        prices = []
        for pfs in pfs_list:
            for price in pfs.fuel_prices:
                if price.fuel_type == fuel_type:
                    prices.append(price)
        return prices

    def get_incremental_updates(self, since_timestamp: str, **kwargs: Any) -> List[PFS]:
        """Get incremental price updates since a specific timestamp."""
        kwargs.setdefault('batch_number', 1)
        return self.get_all_pfs_prices(effective_start_timestamp=since_timestamp, **kwargs)

    def get_all_pfs_prices_paginated(
        self, effective_start_timestamp: Optional[str] = None, use_cache: bool = True
    ) -> List[PFS]:
        """
        Get all PFS fuel prices with automatic pagination.

        Args:
            effective_start_timestamp: Timestamp for incremental updates
            use_cache: Whether to use cached responses

        Returns:
            Complete list of all PFS with fuel prices
        """
        all_pfs = []
        batch = 1
        while True:
            pfs_list = self.get_all_pfs_prices(
                batch_number=batch,
                effective_start_timestamp=effective_start_timestamp,
                use_cache=use_cache,
            )
            if not pfs_list:
                break
            all_pfs.extend(pfs_list)
            if len(pfs_list) < 500:
                break
            batch += 1
        return all_pfs
