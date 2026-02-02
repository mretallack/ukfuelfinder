"""Unit tests for rate limiter module."""
import pytest
import time
from ukfuelfinder.rate_limiter import RateLimiter
from ukfuelfinder.exceptions import RateLimitError


@pytest.mark.unit
class TestRateLimiter:
    """Tests for RateLimiter class."""

    def test_rate_limit_allows_requests(self):
        """Test that requests within limit are allowed."""
        limiter = RateLimiter(requests_per_minute=10, daily_limit=100)

        # Should allow 5 requests without blocking
        for _ in range(5):
            limiter.acquire()  # Should not raise

    def test_daily_limit_exceeded(self):
        """Test that daily limit is enforced."""
        limiter = RateLimiter(requests_per_minute=100, daily_limit=5)

        # Use up daily limit
        for _ in range(5):
            limiter.acquire()

        # Next request should raise
        with pytest.raises(RateLimitError) as exc_info:
            limiter.acquire()

        assert "Daily limit" in str(exc_info.value)
        assert exc_info.value.retry_after > 0

    def test_handle_rate_limit_error(self):
        """Test handling of rate limit errors."""
        limiter = RateLimiter(requests_per_minute=10, daily_limit=100)

        # Should sleep for specified time
        start = time.time()
        limiter.handle_rate_limit_error(retry_after=1)
        elapsed = time.time() - start

        assert elapsed >= 1.0
