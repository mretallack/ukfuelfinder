"""Tests for HTTP client."""

import pytest
from unittest.mock import Mock, patch
from ukfuelfinder.http_client import HTTPClient
from ukfuelfinder.exceptions import (
    BatchNotFoundError,
    NotFoundError,
    RateLimitError,
    ResponseParseError,
    ServerError,
    ValidationError,
)


@pytest.fixture
def mock_authenticator():
    auth = Mock()
    auth.get_token.return_value = "test_token"
    return auth


@pytest.fixture
def mock_rate_limiter():
    limiter = Mock()
    limiter.acquire.return_value = None
    return limiter


@pytest.fixture
def http_client(mock_authenticator, mock_rate_limiter):
    return HTTPClient(
        base_url="https://api.test.com",
        authenticator=mock_authenticator,
        rate_limiter=mock_rate_limiter,
        timeout=30,
    )


def test_successful_request_with_data_wrapper(http_client):
    """Test successful request with new API format (data wrapper)."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": 1}]}
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        result = http_client.get("/test")
        assert result == [{"id": 1}]


def test_successful_request_without_wrapper(http_client):
    """Test successful request with direct data (no wrapper)."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1}]
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        result = http_client.get("/test")
        assert result == [{"id": 1}]


def test_successful_request_old_format(http_client):
    """Test successful request with old API format (success/message fields)."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "message": "",
            "data": [{"id": 1}]
        }
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        result = http_client.get("/test")
        assert result == [{"id": 1}]


def test_batch_not_found_error(http_client):
    """Test 404 on batch endpoint raises BatchNotFoundError."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.url = "https://api.test.com/fuel-prices/999"
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        with pytest.raises(BatchNotFoundError):
            http_client.get("/fuel-prices/999")


def test_not_found_error(http_client):
    """Test 404 on non-batch endpoint raises NotFoundError."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.url = "https://api.test.com/other"
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        with pytest.raises(NotFoundError):
            http_client.get("/other")


def test_validation_error_400(http_client):
    """Test 400 status raises ValidationError."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        with pytest.raises(ValidationError):
            http_client.get("/test")


def test_validation_error_401(http_client):
    """Test 401 status raises ValidationError."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        with pytest.raises(ValidationError):
            http_client.get("/test")


def test_rate_limit_error(http_client):
    """Test 429 status raises RateLimitError."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        with pytest.raises(RateLimitError) as exc_info:
            http_client.get("/test")
        assert exc_info.value.retry_after == 60


def test_server_error(http_client):
    """Test 500 status raises ServerError."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        with pytest.raises(ServerError):
            http_client.get("/test")


def test_response_parse_error(http_client):
    """Test invalid JSON raises ResponseParseError."""
    with patch.object(http_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_request.return_value = mock_response

        with pytest.raises(ResponseParseError):
            http_client.get("/test")
