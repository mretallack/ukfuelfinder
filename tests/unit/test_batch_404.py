"""Mock tests for batch 404 error handling."""

import pytest
from ukfuelfinder.exceptions import BatchNotFoundError


def test_batch_not_found_error():
    """Test BatchNotFoundError exception."""
    error = BatchNotFoundError("Batch 999 not found")
    assert str(error) == "Batch 999 not found"
    assert isinstance(error, BatchNotFoundError)


def test_batch_error_message():
    """Test batch error message format."""
    error = BatchNotFoundError("Batch 123 not found: https://api.example.com/fuel-prices/batch/123")
    assert "Batch 123" in str(error)
    assert "not found" in str(error)
