"""Unit tests for authentication module."""

import pytest
import responses
from ukfuelfinder.auth import OAuth2Authenticator
from ukfuelfinder.exceptions import InvalidCredentialsError


@pytest.mark.unit
class TestOAuth2Authenticator:
    """Tests for OAuth2Authenticator class."""

    @responses.activate
    def test_generate_token_success(self, mock_token_response):
        """Test successful token generation."""
        responses.add(
            responses.POST,
            "https://test.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token",
            json=mock_token_response,
            status=200,
        )

        auth = OAuth2Authenticator(
            client_id="test_id",
            client_secret="test_secret",
            token_url="https://test.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token",
            refresh_url="https://test.fuel-finder.service.gov.uk/api/v1/oauth/regenerate_access_token",
        )

        token = auth.get_token()
        assert token == mock_token_response["access_token"]
        assert auth._refresh_token == mock_token_response["refresh_token"]

    @responses.activate
    def test_token_caching(self, mock_token_response):
        """Test that token is cached and reused."""
        responses.add(
            responses.POST,
            "https://test.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token",
            json=mock_token_response,
            status=200,
        )

        auth = OAuth2Authenticator(
            client_id="test_id",
            client_secret="test_secret",
            token_url="https://test.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token",
            refresh_url="https://test.fuel-finder.service.gov.uk/api/v1/oauth/regenerate_access_token",
        )

        token1 = auth.get_token()
        token2 = auth.get_token()

        assert token1 == token2
        assert len(responses.calls) == 1  # Only one API call

    @responses.activate
    def test_invalid_credentials(self):
        """Test handling of invalid credentials."""
        responses.add(
            responses.POST,
            "https://test.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token",
            json={"error": "invalid_client"},
            status=401,
        )

        auth = OAuth2Authenticator(
            client_id="bad_id",
            client_secret="bad_secret",
            token_url="https://test.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token",
            refresh_url="https://test.fuel-finder.service.gov.uk/api/v1/oauth/regenerate_access_token",
        )

        with pytest.raises(InvalidCredentialsError):
            auth.get_token()

    @responses.activate
    def test_token_refresh(self, mock_token_response):
        """Test token refresh with refresh token."""
        # Initial token
        responses.add(
            responses.POST,
            "https://test.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token",
            json=mock_token_response,
            status=200,
        )

        # Refresh token
        new_token_response = mock_token_response.copy()
        new_token_response["access_token"] = "new_access_token"
        responses.add(
            responses.POST,
            "https://test.fuel-finder.service.gov.uk/api/v1/oauth/regenerate_access_token",
            json=new_token_response,
            status=200,
        )

        auth = OAuth2Authenticator(
            client_id="test_id",
            client_secret="test_secret",
            token_url="https://test.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token",
            refresh_url="https://test.fuel-finder.service.gov.uk/api/v1/oauth/regenerate_access_token",
        )

        # Get initial token
        token1 = auth.get_token()
        assert token1 == mock_token_response["access_token"]

        # Force token expiry
        auth._token_expiry = 0

        # Should refresh
        token2 = auth._refresh_access_token()
        assert token2 == "new_access_token"
