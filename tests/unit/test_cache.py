"""Unit tests for cache module."""

import time

import pytest

from ukfuelfinder.cache import ResponseCache


@pytest.mark.unit
class TestResponseCache:
    """Tests for ResponseCache class."""

    def test_cache_set_and_get(self):
        """Test basic cache storage and retrieval."""
        cache = ResponseCache()
        cache.set("test_key", {"data": "value"}, ttl=60)

        result = cache.get("test_key")
        assert result == {"data": "value"}

    def test_cache_expiry(self):
        """Test that cache entries expire after TTL."""
        cache = ResponseCache()
        cache.set("test_key", {"data": "value"}, ttl=1)

        # Should be available immediately
        assert cache.get("test_key") is not None

        # Wait for expiry
        time.sleep(1.1)

        # Should be expired
        assert cache.get("test_key") is None

    def test_cache_miss(self):
        """Test cache miss returns None."""
        cache = ResponseCache()
        assert cache.get("nonexistent") is None

    def test_cache_clear(self):
        """Test clearing all cache entries."""
        cache = ResponseCache()
        cache.set("key1", "value1", ttl=60)
        cache.set("key2", "value2", ttl=60)

        cache.clear()

        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_generate_key(self):
        """Test cache key generation."""
        cache = ResponseCache()

        key1 = cache.generate_key("/endpoint", {"param": "value"})
        key2 = cache.generate_key("/endpoint", {"param": "value"})
        key3 = cache.generate_key("/endpoint", {"param": "different"})

        assert key1 == key2  # Same params = same key
        assert key1 != key3  # Different params = different key

    def test_cache_stats(self):
        """Test cache statistics tracking."""
        cache = ResponseCache()
        cache.set("key1", "value1", ttl=60)

        # Hit
        cache.get("key1")

        # Miss
        cache.get("key2")

        stats = cache.get_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["total"] == 2
        assert stats["size"] == 1
