"""Unit tests for error handling."""

import pytest
from unittest.mock import Mock, patch
import requests

from ukfuelfinder.http_client import HTTPClient
from ukfuelfinder.exceptions import (
    BatchNotFoundError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    ResponseParseError,
    TimeoutError,
    ConnectionError,
)


class TestErrorHandling:
    """Tests for error handling."""

    @pytest.fixture
    def mock_auth(self):
        """Mock authenticator."""
        auth = Mock()
        auth.get_token.return_value = "test_token"
        return auth

    @pytest.fixture
    def mock_rate_limiter(self):
        """Mock rate limiter."""
        limiter = Mock()
        limiter.acquire.return_value = None
        return limiter

    @pytest.fixture
    def http_client(self, mock_auth, mock_rate_limiter):
        """Create HTTP client with mocked dependencies."""
        return HTTPClient(
            base_url="https://api.example.com",
            authenticator=mock_auth,
            rate_limiter=mock_rate_limiter,
        )

    def test_batch_not_found_error_on_404(self, http_client):
        """Test BatchNotFoundError is raised for 404 on batch endpoints."""
        with patch.object(http_client.session, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.url = "https://api.example.com/fuel-prices/123"
            mock_response.elapsed.total_seconds.return_value = 0.1
            mock_request.return_value = mock_response

            with pytest.raises(BatchNotFoundError, match="Batch not found"):
                http_client.get("/fuel-prices/123")

    def test_not_found_error_on_404_non_batch(self, http_client):
        """Test NotFoundError is raised for 404 on non-batch endpoints."""
        with patch.object(http_client.session, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.url = "https://api.example.com/other/endpoint"
            mock_response.elapsed.total_seconds.return_value = 0.1
            mock_request.return_value = mock_response

            with pytest.raises(NotFoundError, match="Resource not found"):
                http_client.get("/other/endpoint")

    def test_validation_error_on_400(self, http_client):
        """Test ValidationError is raised for 400 responses."""
        with patch.object(http_client.session, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.text = "Invalid parameters"
            mock_response.elapsed.total_seconds.return_value = 0.1
            mock_request.return_value = mock_response

            with pytest.raises(ValidationError, match="Invalid request"):
                http_client.get("/endpoint")

    def test_validation_error_on_401(self, http_client):
        """Test ValidationError is raised for 401 responses."""
        with patch.object(http_client.session, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.elapsed.total_seconds.return_value = 0.1
            mock_request.return_value = mock_response

            with pytest.raises(ValidationError, match="Unauthorized"):
                http_client.get("/endpoint")

    def test_rate_limit_error_on_429(self, http_client):
        """Test RateLimitError is raised for 429 responses."""
        with patch.object(http_client.session, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 429
            mock_response.headers = {"Retry-After": "60"}
            mock_response.elapsed.total_seconds.return_value = 0.1
            mock_request.return_value = mock_response

            with pytest.raises(RateLimitError) as exc_info:
                http_client.get("/endpoint")
            
            assert exc_info.value.retry_after == 60

    def test_server_error_on_500(self, http_client):
        """Test ServerError is raised for 500 responses."""
        with patch.object(http_client.session, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.text = "Internal server error"
            mock_response.elapsed.total_seconds.return_value = 0.1
            mock_request.return_value = mock_response

            with pytest.raises(ServerError, match="Server error: 500"):
                http_client.get("/endpoint")

    def test_response_parse_error_on_invalid_json(self, http_client):
        """Test ResponseParseError is raised for invalid JSON."""
        with patch.object(http_client.session, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_response.elapsed.total_seconds.return_value = 0.1
            mock_request.return_value = mock_response

            with pytest.raises(ResponseParseError, match="Failed to parse JSON"):
                http_client.get("/endpoint")

    def test_timeout_error_after_retries(self, http_client):
        """Test TimeoutError is raised after max retries."""
        with patch.object(http_client.session, "request") as mock_request:
            mock_request.side_effect = requests.Timeout()

            with pytest.raises(TimeoutError, match="timed out"):
                http_client.get("/endpoint")

    def test_connection_error_after_retries(self, http_client):
        """Test ConnectionError is raised after max retries."""
        with patch.object(http_client.session, "request") as mock_request:
            mock_request.side_effect = requests.ConnectionError("Connection failed")

            with pytest.raises(ConnectionError, match="Connection.*failed"):
                http_client.get("/endpoint")

    def test_error_inheritance(self):
        """Test error class inheritance."""
        assert issubclass(BatchNotFoundError, NotFoundError)
        assert issubclass(NotFoundError, Exception)
