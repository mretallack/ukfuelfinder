"""
Response caching for UK Fuel Finder API client.
"""

import time
import threading
import hashlib
import json
from typing import Optional, Dict, Any


class ResponseCache:
    """In-memory cache with TTL support."""

    def __init__(self) -> None:
        self._cache: Dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if time.time() < expiry:
                    self._hits += 1
                    return value
                else:
                    del self._cache[key]

            self._misses += 1
            return None

    def set(self, key: str, value: Any, ttl: int) -> None:
        """Store value in cache with TTL in seconds."""
        with self._lock:
            expiry = time.time() + ttl
            self._cache[key] = (value, expiry)

    def clear(self) -> None:
        """Clear all cached data."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    def generate_key(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Generate cache key from endpoint and parameters."""
        if params:
            # Sort params for consistent key generation
            sorted_params = json.dumps(params, sort_keys=True)
            key_str = f"{endpoint}:{sorted_params}"
        else:
            key_str = endpoint

        return hashlib.md5(key_str.encode()).hexdigest()

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "total": total,
                "hit_rate": round(hit_rate, 2),
                "size": len(self._cache),
            }
