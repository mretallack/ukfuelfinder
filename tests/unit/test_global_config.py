"""Tests for global configuration."""

import os
import pytest
from ukfuelfinder import FuelFinderClient, set_global_backward_compatible
from ukfuelfinder.config import get_global_backward_compatible, _global_backward_compatible


@pytest.fixture(autouse=True)
def reset_global_config():
    """Reset global config before and after each test."""
    import ukfuelfinder.config
    ukfuelfinder.config._global_backward_compatible = None
    yield
    ukfuelfinder.config._global_backward_compatible = None


@pytest.fixture(autouse=True)
def clear_env_var():
    """Clear environment variable before and after each test."""
    if "UKFUELFINDER_BACKWARD_COMPATIBLE" in os.environ:
        del os.environ["UKFUELFINDER_BACKWARD_COMPATIBLE"]
    yield
    if "UKFUELFINDER_BACKWARD_COMPATIBLE" in os.environ:
        del os.environ["UKFUELFINDER_BACKWARD_COMPATIBLE"]


def test_set_global_backward_compatible():
    """Test setting global backward compatibility."""
    set_global_backward_compatible(False)
    assert get_global_backward_compatible() is False
    
    set_global_backward_compatible(True)
    assert get_global_backward_compatible() is True


def test_global_config_overrides_parameter():
    """Test that global config overrides constructor parameter."""
    set_global_backward_compatible(False)
    
    client = FuelFinderClient(
        client_id="test",
        client_secret="test",
        backward_compatible=True  # Should be overridden
    )
    
    assert client.backward_compatible is False


def test_global_config_overrides_env_var():
    """Test that global config overrides environment variable."""
    os.environ["UKFUELFINDER_BACKWARD_COMPATIBLE"] = "true"
    set_global_backward_compatible(False)
    
    client = FuelFinderClient(
        client_id="test",
        client_secret="test"
    )
    
    assert client.backward_compatible is False


def test_env_var_overrides_parameter():
    """Test that environment variable overrides constructor parameter."""
    os.environ["UKFUELFINDER_BACKWARD_COMPATIBLE"] = "false"
    
    client = FuelFinderClient(
        client_id="test",
        client_secret="test",
        backward_compatible=True  # Should be overridden
    )
    
    assert client.backward_compatible is False


def test_parameter_used_when_no_global_or_env():
    """Test that parameter is used when no global config or env var set."""
    client = FuelFinderClient(
        client_id="test",
        client_secret="test",
        backward_compatible=False
    )
    
    assert client.backward_compatible is False


def test_default_parameter_value():
    """Test default parameter value when nothing else is set."""
    client = FuelFinderClient(
        client_id="test",
        client_secret="test"
    )
    
    assert client.backward_compatible is True
