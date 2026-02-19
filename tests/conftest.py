"""Pytest configuration and fixtures."""

import os

import pytest
from dotenv import load_dotenv

from tests.fixtures.responses import MOCK_PFS_RESPONSE, MOCK_TOKEN_RESPONSE
from ukfuelfinder import FuelFinderClient

# Load environment variables from .env file
load_dotenv()


@pytest.fixture
def mock_client():
    """Provide a client with test credentials."""
    return FuelFinderClient(
        client_id="test_client_id", client_secret="test_client_secret", environment="test"
    )


@pytest.fixture
def real_client():
    """Provide a client with real credentials from environment."""
    client_id = os.getenv("FUEL_FINDER_CLIENT_ID")
    client_secret = os.getenv("FUEL_FINDER_CLIENT_SECRET")

    if not client_id or not client_secret:
        pytest.skip("Real API credentials not available")

    return FuelFinderClient(
        client_id=client_id, client_secret=client_secret, environment="production"
    )


@pytest.fixture
def mock_token_response():
    """Provide mock token response."""
    return MOCK_TOKEN_RESPONSE


@pytest.fixture
def mock_pfs_response():
    """Provide mock PFS response."""
    return MOCK_PFS_RESPONSE
