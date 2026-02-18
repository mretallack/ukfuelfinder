"""
Forecourt service for UK Fuel Finder API.
"""

from typing import Any, Dict, Iterator, List, Optional

from ..cache import ResponseCache
from ..http_client import HTTPClient
from ..models import PFSInfo


class ForecourtService:
    """Service for forecourt/PFS information operations."""

    def __init__(self, http_client: HTTPClient, cache: ResponseCache):
        self.http_client = http_client
        self.cache = cache
        self.cache_ttl = 3600  # 1 hour for forecourt info

    def get_all_pfs(
        self, batch_number: Optional[int] = None, use_cache: bool = True
    ) -> List[PFSInfo]:
        """
        Get all PFS information.

        Args:
            batch_number: Batch number for pagination (500 per batch)
            use_cache: Whether to use cached response

        Returns:
            List of PFS information
        """
        params: Dict[str, Any] = {}
        if batch_number:
            params["batch-number"] = batch_number

        cache_key = self.cache.generate_key("/pfs", params)

        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return [PFSInfo.from_dict(item) for item in cached]

        response = self.http_client.get("/pfs", params=params)
        self.cache.set(cache_key, response, self.cache_ttl)

        return [PFSInfo.from_dict(item) for item in response]

    def get_incremental_pfs(
        self,
        effective_start_timestamp: str,
        batch_number: Optional[int] = None,
        use_cache: bool = True,
    ) -> List[PFSInfo]:
        """
        Get incremental PFS information updates.

        Args:
            effective_start_timestamp: Timestamp in YYYY-MM-DD HH:MM:SS format
            batch_number: Batch number for pagination
            use_cache: Whether to use cached response

        Returns:
            List of updated PFS information
        """
        params: Dict[str, Any] = {"effective-start-timestamp": effective_start_timestamp}
        if batch_number:
            params["batch-number"] = batch_number

        cache_key = self.cache.generate_key("/pfs", params)

        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return [PFSInfo.from_dict(item) for item in cached]

        response = self.http_client.get("/pfs", params=params)
        self.cache.set(cache_key, response, self.cache_ttl)

        return [PFSInfo.from_dict(item) for item in response]

    def get_pfs_by_node_id(self, node_id: str, pfs_list: List[PFSInfo]) -> Optional[PFSInfo]:
        """Get specific PFS by node ID from a list."""
        for pfs in pfs_list:
            if pfs.node_id == node_id:
                return pfs
        return None

    def get_all_pfs_paginated(self, use_cache: bool = True) -> Iterator[List[PFSInfo]]:
        """
        Get all PFS information with automatic pagination.

        Yields batches of up to 500 PFS records until no more data is available.

        Args:
            use_cache: Whether to use cached responses

        Yields:
            Lists of PFS information (up to 500 per batch)
        """
        batch = 1
        while True:
            pfs_list = self.get_all_pfs(batch_number=batch, use_cache=use_cache)
            if not pfs_list:
                break
            yield pfs_list
            if len(pfs_list) < 500:
                break
            batch += 1
