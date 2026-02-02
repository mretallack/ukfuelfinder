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
        date_time: Optional[str] = None,
        batch_number: Optional[int] = None,
        effective_start_timestamp: Optional[str] = None,
        use_cache: bool = True,
    ) -> List[PFS]:
        """
        Get all PFS fuel prices.

        Args:
            date_time: Start date in YYYY-MM-DD format for incremental updates
            batch_number: Batch number for pagination
            effective_start_timestamp: Timestamp in YYYY-MM-DD HH:MM:SS format
            use_cache: Whether to use cached response

        Returns:
            List of PFS with fuel prices
        """
        params: Dict[str, Any] = {}
        if date_time:
            params["date_time"] = date_time
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

    def get_incremental_updates(self, since_date: str, **kwargs: Any) -> List[PFS]:
        """Get incremental price updates since a specific date."""
        return self.get_all_pfs_prices(date_time=since_date, **kwargs)
