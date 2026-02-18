"""Integration tests with real API."""

import pytest
from datetime import datetime, timedelta


@pytest.mark.integration
class TestRealAPI:
    """Integration tests using real API credentials."""

    def test_authentication(self, real_client):
        """Test that authentication works with real credentials."""
        # This will authenticate when making first request
        token = real_client.authenticator.get_token()
        assert token is not None
        assert len(token) > 0

    def test_get_all_pfs_prices(self, real_client):
        """Test fetching all PFS fuel prices."""
        prices = real_client.get_all_pfs_prices()

        assert isinstance(prices, list)
        assert len(prices) > 0

        # Check first PFS structure
        pfs = prices[0]
        assert hasattr(pfs, "node_id")
        assert hasattr(pfs, "trading_name")
        assert hasattr(pfs, "fuel_prices")
        assert len(pfs.fuel_prices) > 0

    def test_get_pfs_info(self, real_client):
        """Test fetching PFS information."""
        pfs_list = real_client.get_all_pfs_info(batch_number=1)

        assert isinstance(pfs_list, list)
        assert len(pfs_list) > 0

        # Check first PFS info structure
        pfs = pfs_list[0]
        assert hasattr(pfs, "node_id")
        assert hasattr(pfs, "trading_name")

    def test_incremental_updates(self, real_client):
        """Test fetching incremental price updates."""
        # Get updates from yesterday
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        updates = real_client.get_incremental_price_updates(yesterday)

        assert isinstance(updates, list)
        # May be empty if no updates

    def test_cache_functionality(self, real_client):
        """Test that caching works."""
        # First request
        prices1 = real_client.get_all_pfs_prices()

        # Second request (should be cached)
        prices2 = real_client.get_all_pfs_prices()

        # Should return same data
        assert len(prices1) == len(prices2)

        # Check cache stats
        stats = real_client.get_cache_stats()
        assert stats["hits"] > 0

    def test_clear_cache(self, real_client):
        """Test cache clearing."""
        # Make a request with specific batch to avoid rate limits
        real_client.get_all_pfs_prices(batch_number=1)

        # Clear cache
        real_client.clear_cache()

        # Check cache is empty
        stats = real_client.get_cache_stats()
        assert stats["size"] == 0
