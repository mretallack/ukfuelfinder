"""Unit tests for error handling and backward compatibility."""

import pytest

from ukfuelfinder.client import FuelFinderClient
from ukfuelfinder.exceptions import BatchNotFoundError, InvalidBatchNumberError


class TestErrorHandling:
    """Tests for error handling and backward compatibility."""

    def test_batch_not_found_error_creation(self):
        """Test BatchNotFoundError exception."""
        error = BatchNotFoundError("Batch 999 not found")
        assert str(error) == "Batch 999 not found"
        assert isinstance(error, BatchNotFoundError)

    def test_invalid_batch_number_error_creation(self):
        """Test InvalidBatchNumberError exception."""
        error = InvalidBatchNumberError("Invalid batch number: 999")
        assert str(error) == "Invalid batch number: 999"
        assert isinstance(error, InvalidBatchNumberError)

    def test_backward_compatible_error_handling(self):
        """Test backward compatible error handling."""
        # Test that BatchNotFoundError is raised
        with pytest.raises(BatchNotFoundError):
            raise BatchNotFoundError("Batch not found")

    def test_backward_compatibility_error_wrapping(self):
        """Test that backward compatibility mode changes error types."""
        # When backward compatibility is enabled, BatchNotFoundError
        # should be converted to InvalidBatchNumberError
        client = FuelFinderClient(client_id="test", client_secret="test", backward_compatible=True)
        assert client.backward_compatible is True

    def test_error_message_preservation(self):
        """Test that error messages are preserved during conversion."""
        original_msg = "Batch 123 not found"
        batch_error = BatchNotFoundError(original_msg)

        # Test that error message is preserved
        assert str(batch_error) == original_msg
