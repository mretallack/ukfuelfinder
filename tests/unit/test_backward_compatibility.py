"""Unit tests for backward compatibility."""

import pytest
import warnings
from ukfuelfinder.client import FuelFinderClient
from ukfuelfinder.compatibility import BackwardCompatibleResponse
from ukfuelfinder.models import PFS


@pytest.mark.unit
class TestBackwardCompatibility:
    """Tests for backward compatibility features."""
    
    def test_backward_compatible_response_wrapper(self):
        """Test BackwardCompatibleResponse wrapper."""
        # Create a mock PFS object
        mock_pfs = PFS(
            node_id="test123",
            mft_organisation_name="Test Org",
            trading_name="Test Station",
            public_phone_number="01234567890",
            fuel_prices=[]
        )
        
        # Wrap it
        wrapped = BackwardCompatibleResponse(mock_pfs)
        
        # Test that wrapper provides success and message fields
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert wrapped.success is True
            assert wrapped.message == ""
            assert len(w) == 2  # One warning for each deprecated field access
            assert issubclass(w[0].category, DeprecationWarning)
            assert issubclass(w[1].category, DeprecationWarning)
        
        # Test that wrapper delegates other attributes
        assert wrapped.node_id == "test123"
        assert wrapped.trading_name == "Test Station"
        assert wrapped.public_phone_number == "01234567890"
        
        # Test string representations
        assert "BackwardCompatibleResponse" in repr(wrapped)
        assert "test123" in str(wrapped)
    
    def test_client_backward_compatibility_default(self):
        """Test client backward compatibility defaults to True."""
        client = FuelFinderClient(
            client_id="test_id",
            client_secret="test_secret",
            environment="test"
        )
        assert client.backward_compatible is True
    
    def test_client_backward_compatibility_disabled(self):
        """Test client with backward compatibility disabled."""
        client = FuelFinderClient(
            client_id="test_id",
            client_secret="test_secret",
            environment="test",
            backward_compatible=False
        )
        assert client.backward_compatible is False
    
    def test_client_backward_compatibility_enabled(self):
        """Test client with backward compatibility enabled."""
        client = FuelFinderClient(
            client_id="test_id",
            client_secret="test_secret",
            environment="test",
            backward_compatible=True
        )
        assert client.backward_compatible is True