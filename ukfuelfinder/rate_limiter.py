"""
Rate limiting for UK Fuel Finder API client.
"""

import threading
import time
from collections import deque
from typing import Deque

from .exceptions import RateLimitError


class RateLimiter:
    """Rate limiter with sliding window and exponential backoff."""

    def __init__(self, requests_per_minute: int, daily_limit: int):
        self.requests_per_minute = requests_per_minute
        self.daily_limit = daily_limit
        self._minute_window: Deque[float] = deque()
        self._daily_count = 0
        self._daily_reset = time.time() + 86400  # 24 hours
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Acquire permission to make a request, blocking if necessary."""
        with self._lock:
            self._reset_daily_if_needed()
            self._wait_if_needed()
            self._record_request()

    def _reset_daily_if_needed(self) -> None:
        """Reset daily counter if 24 hours have passed."""
        if time.time() >= self._daily_reset:
            self._daily_count = 0
            self._daily_reset = time.time() + 86400

    def _wait_if_needed(self) -> None:
        """Wait if rate limits would be exceeded."""
        now = time.time()

        # Remove requests older than 1 minute
        while self._minute_window and self._minute_window[0] < now - 60:
            self._minute_window.popleft()

        # Check daily limit
        if self._daily_count >= self.daily_limit:
            wait_time = self._daily_reset - now
            raise RateLimitError(
                f"Daily limit of {self.daily_limit} requests exceeded. "
                f"Resets in {int(wait_time)} seconds",
                retry_after=int(wait_time),
            )

        # Check per-minute limit
        if len(self._minute_window) >= self.requests_per_minute:
            oldest = self._minute_window[0]
            wait_time = 60 - (now - oldest)
            if wait_time > 0:
                time.sleep(wait_time)

    def _record_request(self) -> None:
        """Record a request in the sliding window."""
        now = time.time()
        self._minute_window.append(now)
        self._daily_count += 1

    def handle_rate_limit_error(self, retry_after: int) -> None:
        """Handle 429 rate limit error with exponential backoff."""
        if retry_after > 0:
            time.sleep(retry_after)
        else:
            # Default exponential backoff
            time.sleep(1)
